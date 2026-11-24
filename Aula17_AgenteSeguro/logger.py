import logging, os
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/agente.log', level=logging.INFO,
                   format='%(asctime)s | %(levelname)s | %(message)s', encoding='utf-8')
logger = logging.getLogger('agente')
