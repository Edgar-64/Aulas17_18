import json
from datetime import datetime, timezone

def registrar_evento(evento, status, extras=None):
    dados = {'data': datetime.now(timezone.utc).isoformat(), 'evento': evento, 'status': status}
    if extras and isinstance(extras, dict):
        dados.update(extras)
    with open('logs/eventos.jsonl', 'a', encoding='utf-8') as arquivo:
        arquivo.write(json.dumps(dados, ensure_ascii=False) + '\n')
