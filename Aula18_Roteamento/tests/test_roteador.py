from roteador import selecionar_ferramenta

def test_rotear_calculo():
    assert selecionar_ferramenta('calculo') == 'calculadora'

def test_rotear_horario():
    assert selecionar_ferramenta('horario') == 'relogio'

def test_rotear_pergunta():
    assert selecionar_ferramenta('pergunta') == 'agente'

def test_rotear_invalido():
    assert selecionar_ferramenta('desconhecido') == 'invalido'
