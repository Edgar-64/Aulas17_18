from agente import executar_agente
from ferramentas import executar_ferramenta

def main():
    print('=' * 40)
    print('Agente com Testes e Observabilidade')
    print('1 - Perguntar ao agente')
    print('2 - Usar ferramenta calculadora autorizada')
    print("Digite 'sair' para encerrar.")
    print('=' * 40)
    while True:
        opcao = input('\nOpção: ').strip().lower()
        if opcao == 'sair':
            break
        if opcao == '2':
            try:
                a = float(input('Primeiro número: '))
                b = float(input('Segundo número: '))
                resultado = executar_ferramenta('calcular', {'a': a, 'b': b})
                print('Resultado:', resultado)
            except ValueError:
                print('Erro: informe valores numéricos.')
        elif opcao == '1':
            pergunta = input('Você: ')
            print('Agente:', executar_agente(pergunta))
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    main()
