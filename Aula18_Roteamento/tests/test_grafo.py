import pytest
pytest.importorskip('langgraph')
from grafo import executar_grafo

def test_grafo_calculo():
    assert executar_grafo('calculo', 10, 20) == '30'

def test_grafo_horario():
    resultado = executar_grafo('horario')
    assert isinstance(resultado, str) and len(resultado) == 8

def test_grafo_tipo_invalido():
    assert executar_grafo('nao_existe') == 'Solicitação inválida.'
