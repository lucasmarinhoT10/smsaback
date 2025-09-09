import logging
import os

from dotenv import load_dotenv
from logs.formatters.console_formatter import ConsoleFormatter
from logs.handlers.file_handler import FileWriteHandler
from pythonjsonlogger import json

load_dotenv()


class InfoOnlyConsoleFilter(logging.Filter):
    def filter(self, record):
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        if log_level == "INFO" and record.levelname != "INFO":
            return False
        return True


class EngineLogs:
    """
    A classe EngineLogs serve como um motor centralizado para configuração e gerenciamento de logs na aplicação.
    Ela permite registrar logs em diferentes destinos, como console, arquivos locais, PostgreSQL e MongoDB,
    de acordo com as variáveis de ambiente definidas. O formato e o nível dos logs também podem ser customizados
    facilmente via configuração.

    Como usar:
    1. Instancie a EngineLogs:
           engine_logs = EngineLogs()

    2. Obtenha o logger para uso, podendo passar um contexto extra (opcional):
           logger = engine_logs.get_logger({"user_id": 123, "action": "login"})

    3. Utilize o logger normalmente:
           logger.info("Usuário autenticado com sucesso")
           logger.error("Erro ao processar requisição", extra={"extra": {"detalhe": "timeout"}})

    As variáveis de ambiente controlam os destinos e o nível dos logs, conforme detalhado no README.
    """

    def __init__(self):
        env = os.getenv("ENVIRONMENT", "default")
        level = os.getenv("LOG_LEVEL", "INFO").upper()

        self.logger = logging.getLogger(env)
        self.logger.setLevel(getattr(logging, level, logging.INFO))

        formatter = json.JsonFormatter(
            fmt="Log Level [%(level)s] | %(timestamp)s - %(name)s %(message)s %(user_id)s %(action)s %(extra)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"},
        )

        # Console
        if os.getenv("LOG_CONSOLE", "true").lower() == "true":
            console_handler = logging.StreamHandler()
            console_formatter = ConsoleFormatter()
            console_handler.setFormatter(console_formatter)
            console_handler.addFilter(InfoOnlyConsoleFilter())
            self.logger.addHandler(console_handler)

        # Arquivo local
        if os.getenv("LOG_FILE", "false").lower() == "true":
            file_path = os.getenv("LOG_FILE_PATH", "")
            file_handler = FileWriteHandler(
                file_path, "log", maxBytes=5_000_000, backupCount=3
            )
            self.logger.addHandler(file_handler)

        # # Postgres
        # if os.getenv("LOG_POSTGRES", "false").lower() == "true":
        #     dsn = os.getenv("POSTGRES_URI")
        #     db = os.getenv("POSTGRES_DATABASE")
        #     pg_handler = PostgresHandler(dsn, db)
        #     pg_handler.setFormatter(formatter)
        #     self.logger.addHandler(pg_handler)

        # # Mongo
        # if os.getenv("LOG_MONGO", "false").lower() == "true":
        #     uri = os.getenv("MONGO_URI")
        #     db = os.getenv("MONGO_DB", "logsdb")
        #     coll = os.getenv("MONGO_COLLECTION", "logs")
        #     mongo_handler = MongoHandler(uri, db, coll)
        #     mongo_handler.setFormatter(formatter)
        #     self.logger.addHandler(mongo_handler)

    def get_logger(self, context: dict = None):
        """
        Esta função `get_logger` retorna um LoggerAdapter do Python, que permite adicionar informações de contexto (como user_id, action, etc.) a cada log gerado.
        O parâmetro `context` é um dicionário opcional com dados extras que serão incluídos automaticamente em todas as mensagens de log feitas por esse logger.
        Se nenhum contexto for passado, um dicionário vazio é utilizado.
        """
        return logging.LoggerAdapter(self.logger, context or {})
