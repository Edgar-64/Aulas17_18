from datetime import datetime

def calcular(a, b):
    if type(a) not in (int, float):
        return 'Erro: primeiro valor inválido.'
    if type(b) not in (int, float):
        return 'Erro: segundo valor inválido.'
    return str(a + b)

def consultar_horario():
    return datetime.now().strftime('%H:%M:%S')

def responder_pergunta(pergunta):
    return f'Pergunta recebida: {pergunta}'  # fallback didático quando API não está configurada
