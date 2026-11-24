from ferramentas import calcular, executar_ferramenta

def test_calculo_valido():
    assert calcular(10, 5)['resultado'] == 15

def test_calculo_invalido():
    assert 'erro' in calcular('dez', 5)

def test_ferramenta_nao_autorizada():
    assert executar_ferramenta('apagar_arquivos', {})['erro'] == 'Ferramenta não autorizada.'

def test_argumentos_invalidos():
    assert 'erro' in executar_ferramenta('calcular', {'a': 10})
