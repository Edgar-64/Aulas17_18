from observabilidade import evento

def registrar_log(pergunta, resposta):
    # Log apenas metadados, nunca o conteúdo da conversa.
    evento("interacao_terminal", pergunta_caracteres=len(pergunta), resposta_caracteres=len(resposta))
