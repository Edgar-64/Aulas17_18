from agente import executar_agente

def test_calcular():
    assert executar_agente('calculo', a=10, b=20) == '30'

def test_calculo_argumento_invalido():
    assert executar_agente('calculo', a='dez', b=5) == 'Erro: primeiro valor inválido.'

def test_horario():
    resultado = executar_agente('horario')
    assert isinstance(resultado, str) and len(resultado) == 8 and resultado[2] == ':'

def test_tipo_invalido():
    assert executar_agente('outro') == 'Erro: tipo de solicitação inválido.'
