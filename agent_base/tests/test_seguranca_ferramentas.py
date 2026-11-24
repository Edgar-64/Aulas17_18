import tempfile
from pathlib import Path
import pytest
import ferramentas as f

@pytest.fixture
def banco_temporario(monkeypatch, tmp_path):
    monkeypatch.setattr(f, "DB_TAREFAS", tmp_path / "tarefas_teste.db")
    f.inicializar_tarefas()


def test_registro_consulta_e_conclusao(banco_temporario):
    novo = f.executar_ferramenta("registrar_tarefa", {"descricao":"Revisar Python"})
    assert novo["sucesso"] and novo["id"] == 1
    lista = f.executar_ferramenta("consultar_tarefas", {})
    assert lista[0]["descricao"] == "Revisar Python" and lista[0]["status"] == "pendente"
    assert f.executar_ferramenta("concluir_tarefa", {"tarefa_id":1})["sucesso"]
    assert f.executar_ferramenta("consultar_tarefas", {})[0]["status"] == "concluida"

@pytest.mark.parametrize("descricao", ["", "   ", None, 12])
def test_descricao_invalida(descricao, banco_temporario):
    with pytest.raises(ValueError):
        f.executar_ferramenta("registrar_tarefa", {"descricao":descricao})

def test_bloqueia_tool_nao_autorizada():
    with pytest.raises(ValueError, match="não autorizada"):
        f.executar_ferramenta("excluir_banco", {})

def test_validacao_de_argumentos(banco_temporario):
    with pytest.raises(ValueError):
        f.executar_ferramenta("registrar_tarefa", {"descricao":"ok", "extra":1})
    with pytest.raises(ValueError):
        f.executar_ferramenta("calcular", {"a":1})
    with pytest.raises(ValueError):
        f.executar_ferramenta("consultar_tarefas", {"extra":True})

@pytest.mark.parametrize("id_invalido", [True, 1.2, "1", 0, -1, None])
def test_id_invalido(id_invalido, banco_temporario):
    with pytest.raises(ValueError):
        f.executar_ferramenta("concluir_tarefa", {"tarefa_id":id_invalido})

def test_schemas_json_declarados():
    for tool in f.FERRAMENTAS_AUTORIZADAS:
        assert tool.args_schema is not None
        tool.args_schema.model_json_schema()

@pytest.mark.parametrize("valor", [True, "5", None, 3.2])
def test_calculadora_rejeita_tipo_invalido(valor):
    with pytest.raises(ValueError):
        f.executar_ferramenta("calcular", {"a": valor, "b": 2})
