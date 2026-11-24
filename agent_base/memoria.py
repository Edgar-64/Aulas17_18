import mysql.connector
from config import DB_CONFIG, MAX_HISTORICO


def conectar_banco():
    return mysql.connector.connect(**DB_CONFIG)


def inicializar_memoria():
    """Cria a tabela de histórico caso ainda não exista."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memoria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL
            )
        """)
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


def salvar_mensagem(role, content):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO memoria (role, content) VALUES (%s, %s)",
            (role, content),
        )
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


def recuperar_historico():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        limite = MAX_HISTORICO * 2
        cursor.execute(
            """
            SELECT role, content
            FROM memoria
            ORDER BY id DESC
            LIMIT %s
            """,
            (limite,),
        )
        resultados = cursor.fetchall()
        resultados.reverse()
        return [
            {"role": role, "content": content}
            for role, content in resultados
            if role in ("user", "assistant")
        ]
    finally:
        cursor.close()
        conexao.close()
