import time
from config import API_KEY, MODEL, INSTRUCOES
from logger import logger
from eventos_json import registrar_evento

def validar_pergunta(pergunta):
    return isinstance(pergunta, str) and bool(pergunta.strip()) and len(pergunta) <= 500

def executar_agente(pergunta, consultar_modelo=None):
    inicio = time.perf_counter()
    logger.info('Nova execução iniciada')
    registrar_evento('execucao_agente', 'iniciada')
    if not validar_pergunta(pergunta):
        logger.warning('Entrada inválida')
        registrar_evento('validacao_entrada', 'rejeitada')
        return 'Erro: pergunta inválida.'
    try:
        if consultar_modelo is None:
            if not API_KEY:
                raise ValueError('API não configurada')
            from groq import Groq
            client = Groq(api_key=API_KEY)
            def consultar_modelo(texto):
                resposta = client.chat.completions.create(model=MODEL, messages=[
                    {'role': 'system', 'content': INSTRUCOES},
                    {'role': 'user', 'content': texto}])
                return resposta.choices[0].message.content
        resposta = consultar_modelo(pergunta)
        if not isinstance(resposta, str) or not resposta.strip():
            raise ValueError('Resposta inválida do modelo')
        logger.info('Execução concluída com sucesso')
        registrar_evento('execucao_agente', 'sucesso')
        return resposta
    except Exception as erro:
        logger.error('Falha na execução: %s', type(erro).__name__)
        registrar_evento('execucao_agente', 'erro', {'tipo_erro': type(erro).__name__})
        return 'Erro ao consultar o agente.'
    finally:
        duracao = time.perf_counter() - inicio
        logger.info('Tempo de execução: %.3f segundos', duracao)
        registrar_evento('duracao_execucao', 'registrada', {'duracao_ms': round(duracao * 1000, 2)})
