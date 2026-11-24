from agente import responder

def test_rejeita_pergunta_vazia():
    assert responder("   ") == "Digite uma pergunta válida."

def test_rejeita_pergunta_excessivamente_longa():
    resposta = responder("x" * 5001)
    assert "5000 caracteres" in resposta
