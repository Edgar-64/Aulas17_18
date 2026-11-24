from agente import validar_pergunta, executar_agente

def test_pergunta_valida():
    assert validar_pergunta('O que é Python?') is True

def test_pergunta_vazia():
    assert validar_pergunta('') is False

def test_pergunta_muito_longa():
    assert validar_pergunta('a' * 501) is False

def test_resposta_simulada():
    assert executar_agente('Olá', lambda p: 'Resposta de teste') == 'Resposta de teste'

def test_falha_da_api():
    def modelo_com_erro(pergunta):
        raise ConnectionError('API indisponível')
    assert executar_agente('Olá', modelo_com_erro) == 'Erro ao consultar o agente.'
