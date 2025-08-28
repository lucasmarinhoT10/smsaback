import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import json
import os
from datetime import datetime

from ..formatters.file_formatter import FileJsonFormatter

class FileJSONHandler(RotatingFileHandler):
    def __init__(self, base_path, file_type, maxBytes=5_000_000, backupCount=3):
        # Garante que o diretório existe, se não existir, cria
        dir_path = os.path.dirname(base_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # Usa base_path apenas como caminho, nome do arquivo será dinâmico
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(
            dir_path,
            f"{timestamp}.{file_type}"
        ) if dir_path else f"{timestamp}.{file_type}"

        super().__init__(file_path, maxBytes=maxBytes, backupCount=backupCount, encoding="utf-8")

        # Formatter corrigido
        self.json_formatter = FileJsonFormatter()
        self.setFormatter(self.json_formatter)

    def emit(self, record):
        # garante que asctime esteja sempre preenchido
        if not hasattr(record, "asctime"):
            record.asctime = self.json_formatter.formatTime(record, "%Y-%m-%dT%H:%M:%S")
        super().emit(record)