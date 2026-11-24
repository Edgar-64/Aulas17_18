from typing import Annotated, TypedDict, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from config import INSTRUCOES
from ferramentas import FERRAMENTAS_AUTORIZADAS
from memoria import recuperar_historico, salvar_mensagem
from modelo import criar_modelo
from roteador import identificar_rota
from observabilidade import evento, Cronometro


class EstadoAgente(TypedDict):
    messages: Annotated[list, add_messages]
    rota: Optional[str]




def identificar_intencao(estado: EstadoAgente):
    mensagem = next((m for m in reversed(estado["messages"]) if isinstance(m, HumanMessage)), None)
    rota = identificar_rota(mensagem.content if mensagem else "")
    evento("roteamento", rota=rota)
    return {"rota": rota}



def chamar_modelo(estado: EstadoAgente):
    modelo_com_ferramentas = criar_modelo(FERRAMENTAS_AUTORIZADAS)
    rota = estado.get("rota", "pergunta")
    contexto_rota = f"Intenção identificada pelo roteador: {rota}. Use a ferramenta adequada se a solicitação exigir; a classificação é apenas uma indicação e não substitui sua interpretação."
    mensagens = list(estado["messages"])
    mensagens.append(SystemMessage(content=contexto_rota))
    ultima = next((m for m in reversed(mensagens) if isinstance(m, HumanMessage)), None)
    resposta = modelo_com_ferramentas.invoke(mensagens)
    chamadas = getattr(resposta, "tool_calls", []) or []
    evento("modelo_respondeu", rota=rota, ferramentas_solicitadas=[c.get("name") for c in chamadas])
    return {"messages": [resposta]}


def executar_ferramentas(estado: EstadoAgente):
    nomes = []
    for msg in estado.get("messages", []):
        if isinstance(msg, AIMessage):
            nomes.extend(c.get("name", "desconhecida") for c in (msg.tool_calls or []))
    evento("ferramentas_executando", ferramentas=nomes)
    resultado = ToolNode(FERRAMENTAS_AUTORIZADAS).invoke(estado)
    evento("ferramentas_finalizadas", ferramentas=nomes)
    return resultado


def construir_agente():
    """Grafo: roteador -> modelo -> (ferramentas autorizadas -> modelo) ou fim."""
    fluxo = StateGraph(EstadoAgente)
    fluxo.add_node("roteador", identificar_intencao)
    fluxo.add_node("agente", chamar_modelo)
    fluxo.add_node("ferramentas", executar_ferramentas)
    fluxo.add_edge(START, "roteador")
    fluxo.add_edge("roteador", "agente")
    fluxo.add_conditional_edges("agente", tools_condition, {"tools": "ferramentas", END: END})
    fluxo.add_edge("ferramentas", "agente")
    return fluxo.compile()



agente = construir_agente()


def responder(pergunta: str) -> str:
    """Executa agente, valida a entrada, registra eventos/duração e persiste o histórico."""
    cronometro = Cronometro()
    if not isinstance(pergunta, str) or not pergunta.strip():
        evento("entrada_invalida", motivo="pergunta vazia ou não textual")
        return "Digite uma pergunta válida."
    if len(pergunta) > 5000:
        evento("entrada_invalida", motivo="pergunta excedeu limite", caracteres=len(pergunta))
        return "A pergunta excede o limite de 5000 caracteres. Envie uma mensagem menor."
    pergunta = pergunta.strip()
    evento("execucao_iniciada", caracteres=len(pergunta))
    try:
        historico = recuperar_historico()
        mensagens = [SystemMessage(content=INSTRUCOES)]
        for item in historico:
            if item["role"] == "user":
                mensagens.append(HumanMessage(content=item["content"]))
            elif item["role"] == "assistant":
                mensagens.append(AIMessage(content=item["content"]))
        mensagens.append(HumanMessage(content=pergunta))
        resultado = agente.invoke({"messages": mensagens, "rota": "pergunta"}, config={"recursion_limit": 16})
        ultima_resposta = next((m.content for m in reversed(resultado["messages"])
            if isinstance(m, AIMessage) and isinstance(m.content, str) and m.content.strip()),
            "Não consegui gerar uma resposta.")
        salvar_mensagem("user", pergunta)
        salvar_mensagem("assistant", ultima_resposta)
        evento("execucao_concluida", duracao_segundos=cronometro.segundos())
        return ultima_resposta
    except Exception as erro:
        evento("execucao_falhou", erro=type(erro).__name__, duracao_segundos=cronometro.segundos())
        return "Ocorreu um erro ao executar o agente. Verifique os logs para detalhes técnicos."
