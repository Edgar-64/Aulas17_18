"""Testes locais da Aula 17. Não fazem chamadas à API Groq nem exigem MySQL."""
import os
import tempfile
from pathlib import Path

import ferramentas as f


def executar_testes():
    # Usa um banco temporário para não alterar as tarefas reais do usuário.
    banco_original = f.DB_TAREFAS
    with tempfile.TemporaryDirectory() as pasta:
        f.DB_TAREFAS = Path(pasta) / "teste_tarefas.db"
        try:
            primeiro = f.executar_ferramenta(
                "registrar_tarefa", {"descricao": "Estudar Python"}
            )
            assert primeiro["sucesso"] is True
            assert primeiro["id"] == 1

            segundo = f.executar_ferramenta(
                "registrar_tarefa", {"descricao": "Aprender SQL"}
            )
            assert segundo["id"] == 2

            tarefas = f.executar_ferramenta("consultar_tarefas", {})
            assert len(tarefas) == 2
            assert tarefas[0]["descricao"] == "Estudar Python"

            # Validação explícita dos casos inválidos exigidos.
            for descricao in ("", "   ", 123, None):
                try:
                    f.executar_ferramenta(
                        "registrar_tarefa", {"descricao": descricao}
                    )
                    raise AssertionError(f"Descrição inválida aceita: {descricao!r}")
                except ValueError:
                    pass

            try:
                f.executar_ferramenta("ferramenta_inexistente", {})
                raise AssertionError("Ferramenta desconhecida foi aceita.")
            except ValueError:
                pass

            concluida = f.executar_ferramenta(
                "concluir_tarefa", {"tarefa_id": 1}
            )
            assert concluida["sucesso"] is True
            assert f.executar_ferramenta("consultar_tarefas", {})[0]["status"] == "concluida"

            inexistente = f.executar_ferramenta(
                "concluir_tarefa", {"tarefa_id": 999}
            )
            assert inexistente["sucesso"] is False

            for id_invalido in (True, 1.5, "1", 0, -2):
                try:
                    f.executar_ferramenta(
                        "concluir_tarefa", {"tarefa_id": id_invalido}
                    )
                    raise AssertionError(f"ID inválido aceito: {id_invalido!r}")
                except ValueError:
                    pass

            # Confere que as ferramentas têm schemas JSON declarados.
            for ferramenta in f.FERRAMENTAS_AUTORIZADAS:
                assert ferramenta.args_schema is not None
                ferramenta.args_schema.model_json_schema()

            print("Todos os testes da Aula 17 passaram!")
            print("- Cadastro e consulta de tarefas")
            print("- Validação de descrição vazia e tipo inválido")
            print("- Bloqueio de ferramenta não autorizada")
            print("- Conclusão de tarefa e ID inexistente")
            print("- Validação de ID e schemas JSON")
        finally:
            f.DB_TAREFAS = banco_original


if __name__ == "__main__":
    executar_testes()
