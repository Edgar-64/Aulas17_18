import pytest
from roteador import identificar_rota

@pytest.mark.parametrize("texto,rota", [
    ("Quanto é 20 + 30?", "calculo"),
    ("Calcule a divisão de 10 por 2", "calculo"),
    ("Que horas são agora?", "horario"),
    ("Qual a data de hoje?", "horario"),
    ("Registre uma tarefa para estudar Python", "tarefas"),
    ("Liste minhas tarefas", "tarefas"),
    ("Explique o que é LangGraph", "pergunta"),
])
def test_identifica_rota(texto, rota):
    assert identificar_rota(texto) == rota

def test_pergunta_vazia_rejeitada():
    with pytest.raises(ValueError):
        identificar_rota("  ")
