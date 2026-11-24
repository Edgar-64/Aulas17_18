# Aula 18 — Roteamento condicional e orquestração de ferramentas

Implementa a atividade prática: recebe tipos de solicitações, seleciona ferramenta por roteador, valida argumentos numéricos, executa calculadora/relógio/LLM, trata tipos desconhecidos, organiza módulos e inclui um fluxo condicional LangGraph, além de testes Pytest.

## Instalação e uso
1. `python -m venv .venv` e ative o ambiente.
2. `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e insira a chave Groq para habilitar respostas reais. Sem chave, perguntas ao agente usam fallback simulado.
4. `python main.py` para menu interativo.
5. `python -m pytest -v` para testes.
6. O grafo também pode ser executado diretamente: `python -c "from grafo import executar_grafo; print(executar_grafo('calculo', 10, 20))"` (após instalar LangGraph).

O roteamento da atividade usa tipos explícitos escolhidos pelo menu, como no material. O desafio de classificar linguagem natural com LLM é adicional e não foi implementado para não alterar o escopo da atividade principal.
