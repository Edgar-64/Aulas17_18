# Aula 17 — Agente seguro e monitorado

Implementa a atividade prática da Aula 17: valida entradas, consulta Groq (ou função simulada nos testes), trata falhas, registra eventos em logs, mede duração, protege a chave em `.env`, restringe ferramenta autorizada e usa Pytest. Também inclui o desafio adicional de log estruturado JSONL.


## Instalação e execução
1. Instale Python 3.10+.
2. `python -m venv .venv` e ative o ambiente.
3. `pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e preencha `GROQ_API_KEY` para usar o modelo real (não é necessária para testes).
5. `python main.py`
6. Testes: `python -m pytest -v`

Logs são gravados em `logs/agente.log` e `logs/eventos.jsonl`. Não compartilhe o `.env`.
