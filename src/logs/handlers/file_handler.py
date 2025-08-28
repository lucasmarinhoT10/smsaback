import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import json
import os
from datetime import datetime

from ..formatters.file_formatter import FileJsonFormatter

class FileWriteHandler(RotatingFileHandler):
    """
    FileWriteHandler é uma classe personalizada que herda de RotatingFileHandler e serve para gerenciar a escrita de logs em arquivos locais no formato JSON, com rotação automática dos arquivos quando atingem um tamanho máximo.

    - O nome do arquivo é gerado dinamicamente com base no timestamp atual, garantindo que cada execução/criação de handler gere um arquivo único.
    - O diretório de destino é criado automaticamente caso não exista.
    - Utiliza um formatter customizado (FileJsonFormatter) para garantir que os logs sejam gravados em formato JSON.
    - Permite configurar o tamanho máximo do arquivo (maxBytes) e a quantidade de backups (backupCount) a serem mantidos.

    Parâmetros:
        base_path (str): Caminho base onde os arquivos de log serão salvos.
        file_type (str): Extensão/tipo do arquivo de log (ex: 'log', 'json').
        maxBytes (int): Tamanho máximo do arquivo antes da rotação.
        backupCount (int): Quantidade de arquivos de backup a manter.
    """
    def __init__(self, base_path, file_type, maxBytes=5_000_000, backupCount=3):
        dir_path = os.path.dirname(base_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(
            dir_path,
            f"{timestamp}.{file_type}"
        ) if dir_path else f"{timestamp}.{file_type}"

        super().__init__(file_path, maxBytes=maxBytes, backupCount=backupCount, encoding="utf-8")

        self.json_formatter = FileJsonFormatter()
        self.setFormatter(self.json_formatter)

    def emit(self, record):
        """
        O método emit é responsável por efetivamente gravar o registro de log no arquivo.
        Antes de gravar, garante que o campo 'asctime' (timestamp do log) esteja presente no registro,
        utilizando o formatter customizado para formatar o tempo no padrão ISO.
        Em seguida, chama o método emit da superclasse para realizar a escrita.
        """
        if not hasattr(record, "asctime"):
            record.asctime = self.json_formatter.formatTime(record, "%Y-%m-%dT%H:%M:%S")
        super().emit(record)