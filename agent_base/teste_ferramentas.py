from ferramentas import calcular, obter_data, registrar_tarefa, consultar_tarefas, concluir_tarefa


def executar_testes():
    data = obter_data.invoke({})
    assert isinstance(data, str) and data

    resultado = calcular.invoke({"a": 10, "b": 2})
    assert resultado["soma"] == 12
    assert resultado["subtracao"] == 8
    assert resultado["multiplicacao"] == 20
    assert resultado["divisao"] == 5
    assert calcular.invoke({"a": 10, "b": 0})["divisao"] == "Não é possível dividir por zero"

    print("Testes básicos de data e calculadora: OK")


if __name__ == "__main__":
    executar_testes()
