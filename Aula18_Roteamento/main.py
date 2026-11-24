from agente import executar_agente

def main():
    while True:
        print('\n1 - Calcular\n2 - Consultar horário\n3 - Perguntar ao agente\n0 - Sair')
        opcao = input('Escolha: ').strip()
        if opcao == '0':
            break
        try:
            if opcao == '1':
                a = float(input('Primeiro número: '))
                b = float(input('Segundo número: '))
                resposta = executar_agente('calculo', a=a, b=b)
            elif opcao == '2':
                resposta = executar_agente('horario')
            elif opcao == '3':
                pergunta = input('Pergunta: ').strip()
                if not pergunta:
                    resposta = 'Erro: pergunta vazia.'
                else:
                    resposta = executar_agente('pergunta', pergunta=pergunta)
            else:
                resposta = 'Opção inválida.'
        except ValueError:
            resposta = 'Erro: digite valores numéricos válidos.'
        print('Resultado:', resposta)

if __name__ == '__main__':
    main()
