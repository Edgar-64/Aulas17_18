import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool

# O histórico do agente continua no MySQL. As tarefas da Aula 17 ficam
# em um banco SQLite separado, simples e persistente.
DB_TAREFAS = Path(__file__).resolve().parent / "tarefas.db"


@contextmanager
def conectar_tarefas():
    """Abre, confirma (ou desfaz) e SEMPRE fecha a conexão SQLite."""
    conexao = sqlite3.connect(DB_TAREFAS)
    conexao.row_factory = sqlite3.Row
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def inicializar_tarefas():
    with conectar_tarefas() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendente'
            )
        """)
        conexao.commit()


def _validar_descricao(descricao):
    if not isinstance(descricao, str):
        raise ValueError("A descrição da tarefa deve ser um texto.")
    descricao = descricao.strip()
    if not descricao:
        raise ValueError("A descrição da tarefa não pode ficar vazia.")
    return descricao


def _validar_id(tarefa_id):
    # bool é subclasse de int em Python; por isso é rejeitado explicitamente.
    if isinstance(tarefa_id, bool) or not isinstance(tarefa_id, int):
        raise ValueError("O ID da tarefa deve ser um número inteiro válido.")
    if tarefa_id <= 0:
        raise ValueError("O ID da tarefa deve ser maior que zero.")
    return tarefa_id


def _registrar_tarefa(descricao):
    descricao = _validar_descricao(descricao)
    inicializar_tarefas()
    with conectar_tarefas() as conexao:
        cursor = conexao.execute(
            "INSERT INTO tarefas (descricao) VALUES (?)", (descricao,)
        )
        conexao.commit()
        return {
            "sucesso": True,
            "id": cursor.lastrowid,
            "descricao": descricao,
            "status": "pendente",
            "mensagem": f"Tarefa '{descricao}' registrada com sucesso.",
        }


def _consultar_tarefas():
    inicializar_tarefas()
    with conectar_tarefas() as conexao:
        linhas = conexao.execute(
            "SELECT id, descricao, status FROM tarefas ORDER BY id"
        ).fetchall()
    return [dict(linha) for linha in linhas]


def _concluir_tarefa(tarefa_id):
    tarefa_id = _validar_id(tarefa_id)
    inicializar_tarefas()
    with conectar_tarefas() as conexao:
        cursor = conexao.execute(
            "UPDATE tarefas SET status = 'concluida' WHERE id = ?",
            (tarefa_id,),
        )
        conexao.commit()
        if cursor.rowcount == 0:
            return {
                "sucesso": False,
                "mensagem": f"Não existe tarefa com o ID {tarefa_id}.",
            }
    return {
        "sucesso": True,
        "id": tarefa_id,
        "status": "concluida",
        "mensagem": f"Tarefa {tarefa_id} concluída com sucesso.",
    }


@tool
def obter_data() -> str:
    """Retorna a data e o horário atuais do computador."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@tool
def calcular(a: float, b: float) -> dict:
    """Calcula soma, subtração, multiplicação e divisão de dois números."""
    if isinstance(a, bool) or not isinstance(a, (int, float)):
        return {"erro": "O primeiro argumento deve ser numérico."}
    if isinstance(b, bool) or not isinstance(b, (int, float)):
        return {"erro": "O segundo argumento deve ser numérico."}
    return {
        "soma": a + b,
        "subtracao": a - b,
        "multiplicacao": a * b,
        "divisao": a / b if b != 0 else "Não é possível dividir por zero",
    }


@tool
def registrar_tarefa(descricao: str) -> dict:
    """Registra uma nova tarefa pendente no banco SQLite. Informe a descrição."""
    return _registrar_tarefa(descricao)


@tool
def consultar_tarefas() -> list:
    """Consulta e retorna todas as tarefas registradas, com ID e status."""
    return _consultar_tarefas()


@tool
def concluir_tarefa(tarefa_id: int) -> dict:
    """Marca uma tarefa como concluída usando o ID numérico dela."""
    return _concluir_tarefa(tarefa_id)


# Lista de permissões: o LangGraph só recebe ferramentas declaradas aqui.
FERRAMENTAS_AUTORIZADAS = [
    obter_data,
    calcular,
    registrar_tarefa,
    consultar_tarefas,
    concluir_tarefa,
]
FERRAMENTAS_POR_NOME = {f.name: f for f in FERRAMENTAS_AUTORIZADAS}


def executar_ferramenta(nome, argumentos):
    """Executor direto para validar argumentos e controlar a lista de permissões."""
    if nome not in FERRAMENTAS_POR_NOME:
        raise ValueError(f"Ferramenta não autorizada: {nome}")
    if not isinstance(argumentos, dict):
        raise ValueError("Os argumentos da ferramenta devem estar em um objeto.")

    # Validação explícita, independente da validação automática do modelo.
    if nome == "registrar_tarefa":
        if set(argumentos) != {"descricao"}:
            raise ValueError("Informe somente o argumento 'descricao'.")
        return _registrar_tarefa(argumentos["descricao"])
    if nome == "consultar_tarefas":
        if argumentos:
            raise ValueError("A consulta de tarefas não recebe argumentos.")
        return _consultar_tarefas()
    if nome == "concluir_tarefa":
        if set(argumentos) != {"tarefa_id"}:
            raise ValueError("Informe o argumento 'tarefa_id'.")
        return _concluir_tarefa(argumentos["tarefa_id"])
    if nome == "obter_data":
        if argumentos:
            raise ValueError("A ferramenta obter_data não recebe argumentos.")
        return obter_data.invoke({})
    if nome == "calcular":
        if set(argumentos) != {"a", "b"}:
            raise ValueError("Informe os argumentos 'a' e 'b'.")
        for chave in ("a", "b"):
            valor = argumentos[chave]
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise ValueError(f"O argumento '{chave}' deve ser numérico.")
        return calcular.invoke(argumentos)

    raise ValueError(f"Ferramenta não autorizada: {nome}")
