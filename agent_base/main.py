from agente import responder
from ferramentas import inicializar_tarefas
from logs import registrar_log
from memoria import inicializar_memoria


def executar():
    inicializar_memoria()
    inicializar_tarefas()

    print("=" * 54)
    print("       AGENTE DE IA - AULAS 16 A 18")
    print("=" * 54)
    print("Olá! Sou seu assistente de Tecnologia da Informação.")
    print("Posso consultar data/hora, fazer cálculos e gerenciar tarefas.")
    print("Exemplos: 'registre estudar Python', 'liste minhas tarefas'.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() == "sair":
            print("\nAgente: Até mais! Bons estudos!")
            break
        if not pergunta:
            continue
        try:
            resposta = responder(pergunta)
            registrar_log(pergunta, resposta)
            print("\nAgente:", resposta, "\n")
        except Exception as erro:
            print(f"\nOcorreu um erro ao consultar o agente: {erro}\n")


if __name__ == "__main__":
    executar()
