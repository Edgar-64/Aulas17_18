# Ativ2 — Agente Orquestrador (Aulas 16, 17 e 18)

Esta versão evolui a base existente: LangGraph + Groq, memória MySQL/XAMPP, tarefas SQLite e ferramentas autorizadas. Não substitui o projeto por um agente novo.

## Preservado
- Agente LangGraph com ciclo de tool calling.
- Groq via `langchain-groq` e modelo definido por `GROQ_MODEL`.
- Memória/histórico de chat no MySQL.
- Tarefas persistidas em SQLite (`tarefas.db`): registrar, consultar e concluir.
- Ferramentas: data/hora, calculadora, registrar/listar/concluir tarefas.

## Aula 17 incorporada
- Validação de entrada: texto, não vazio e limite de 5000 caracteres.
- Validação de argumentos da calculadora e das ferramentas de tarefa.
- Allowlist de ferramentas.
- Tratamento de exceções sem expor detalhes técnicos na conversa.
- Logging rotativo em `logs/agente.log`, com eventos JSON e duração.
- Logs não registram prompts, respostas, credenciais ou conteúdo de conversas.
- Testes automatizados Pytest (incluindo simulação sem chamada externa para Groq/MySQL).

## Aula 18 incorporada
- Módulo `roteador.py`: classifica a intenção inicial (cálculo, horário, tarefas ou pergunta geral) por regras simples.
- Nó `roteador` integrado ao grafo LangGraph; a classificação serve como indicação contextual para o LLM, não como substituto da interpretação.
- Fluxo do grafo: início → roteador → agente → (ferramentas autorizadas → agente) ou fim.
- Ferramentas continuam separadas da lógica de roteamento e da resposta do modelo.

## Estrutura
- `agente.py`: grafo e execução do agente
- `roteador.py`: identificação de intenção
- `ferramentas.py`: ferramentas, validação, allowlist e SQLite
- `observabilidade.py`: logger rotativo e cronômetro
- `memoria.py`: persistência do histórico MySQL
- `modelo.py`: criação do modelo Groq com tools
- `config.py`: configurações e instruções
- `main.py`: terminal
- `tests/`: testes Pytest

## Instalação e configuração
1. Extraia o ZIP e abra a pasta no VS Code.
2. Ative seu ambiente virtual.
3. Instale dependências: `python -m pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e mantenha as credenciais apenas no `.env`.
5. Inicie o MySQL no XAMPP e confirme que o banco `agente_ativ2` (ou seu DB_NAME configurado) existe.
6. Execute os testes: `python -m pytest -v`
7. Inicie: `python main.py`

## .env
Veja `.env.example`. Não compartilhe seu arquivo `.env` real.


## Testes
Os testes de roteador não usam API nem banco. Os testes de ferramentas usam banco SQLite temporário. Os testes de validação do agente apenas verificam rejeição de entrada inválida e não fazem chamada ao LLM.
