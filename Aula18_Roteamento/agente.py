from config import API_KEY, MODEL
from ferramentas import calcular, consultar_horario, responder_pergunta
from roteador import selecionar_ferramenta

def responder_com_llm(pergunta):
    if not API_KEY:
        return 'GROQ_API_KEY não configurada. Resposta simulada: ' + responder_pergunta(pergunta)
    from groq import Groq
    client = Groq(api_key=API_KEY)
    resposta = client.chat.completions.create(model=MODEL, messages=[
        {'role': 'system', 'content': 'Você é um assistente educacional.'},
        {'role': 'user', 'content': pergunta}])
    return resposta.choices[0].message.content

def executar_agente(tipo, pergunta='', a=None, b=None):
    ferramenta = selecionar_ferramenta(tipo)
    if ferramenta == 'calculadora':
        return calcular(a, b)
    if ferramenta == 'relogio':
        return consultar_horario()
    if ferramenta == 'agente':
        return responder_com_llm(pergunta)
    return 'Erro: tipo de solicitação inválido.'
