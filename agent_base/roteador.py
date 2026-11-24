"""Roteamento determinístico inicial: identifica a intenção provável para orientar o agente."""
from typing import Literal



TipoRota = Literal["calculo", "horario", "tarefas", "pergunta"]


def identificar_rota(pergunta: str) -> TipoRota:
    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta deve ser um texto não vazio.")
    texto = pergunta.casefold()
    termos_calculo = ("calcule", "quanto é", "soma", "somar", "divid", "multiplic", "subtr", " vezes ", " + ", " - ", " * ", " / ")
    termos_horario = ("que horas", "horário atual", "horario atual", "data de hoje", "que dia é", "que dia e", "data e hora")
    termos_tarefas = ("tarefa", "tarefas", "to-do", "todo list", "pendência", "pendencia")
    if any(t in texto for t in termos_calculo):
        return "calculo"
    if any(t in texto for t in termos_horario):
        return "horario"
    if any(t in texto for t in termos_tarefas):
        return "tarefas"
    return "pergunta"
