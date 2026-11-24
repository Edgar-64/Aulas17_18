"""Logging operacional e métricas simples do agente (sem registrar prompts ou segredos)."""
import json
import logging
import time
from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("agente")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    handler = RotatingFileHandler(LOG_DIR / "agente.log", maxBytes=512_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)


def evento(tipo: str, **dados):
    """Registra evento e campos operacionais; evite conteúdo pessoal ou credenciais."""
    campos = {"evento": tipo, **dados}
    logger.info(json.dumps(campos, ensure_ascii=False, default=str))


class Cronometro:
    def __init__(self):
        self.inicio = time.perf_counter()

    def segundos(self):
        return round(time.perf_counter() - self.inicio, 4)
