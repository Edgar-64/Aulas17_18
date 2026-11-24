def selecionar_ferramenta(tipo):
    ferramentas = {'calculo': 'calculadora', 'horario': 'relogio', 'pergunta': 'agente'}
    return ferramentas.get(tipo, 'invalido')
