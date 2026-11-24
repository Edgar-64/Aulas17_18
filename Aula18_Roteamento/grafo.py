from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from ferramentas import calcular, consultar_horario

class Estado(TypedDict):
    tipo: str
    a: float
    b: float
    resposta: str

def roteador(estado):
    return {}

def escolher_caminho(estado):
    if estado.get('tipo') == 'calculo':
        return 'calculadora'
    if estado.get('tipo') == 'horario':
        return 'relogio'
    return 'erro'

def calculadora(estado):
    return {'resposta': calcular(estado.get('a'), estado.get('b'))}

def relogio(estado):
    return {'resposta': consultar_horario()}

def erro(estado):
    return {'resposta': 'Solicitação inválida.'}

grafo_builder = StateGraph(Estado)
grafo_builder.add_node('roteador', roteador)
grafo_builder.add_node('calculadora', calculadora)
grafo_builder.add_node('relogio', relogio)
grafo_builder.add_node('erro', erro)
grafo_builder.add_edge(START, 'roteador')
grafo_builder.add_conditional_edges('roteador', escolher_caminho, {
    'calculadora': 'calculadora', 'relogio': 'relogio', 'erro': 'erro'})
grafo_builder.add_edge('calculadora', END)
grafo_builder.add_edge('relogio', END)
grafo_builder.add_edge('erro', END)
app = grafo_builder.compile()

def executar_grafo(tipo, a=0, b=0):
    estado = {'tipo': tipo, 'a': a, 'b': b, 'resposta': ''}
    return app.invoke(estado)['resposta']
