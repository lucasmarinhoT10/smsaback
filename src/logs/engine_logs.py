import logging
import os
from pythonjsonlogger import json
from dotenv import load_dotenv

from logs.handlers.postgres_handler import PostgresHandler
from logs.handlers.mongo_handler import MongoHandler
from logs.handlers.file_handler import FileJSONHandler
from logs.formatters.console_formatter import ConsoleFormatter

load_dotenv()

class InfoOnlyConsoleFilter(logging.Filter):
    def filter(self, record):
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        if log_level == "INFO" and record.levelname != "INFO":
            return False
        return True

class EngineLogs:
    def __init__(self):
        env = os.getenv("ENVIRONMENT", "default")
        level = os.getenv("LOG_LEVEL", "INFO").upper()

        self.logger = logging.getLogger(env)
        self.logger.setLevel(getattr(logging, level, logging.INFO))

        formatter = json.JsonFormatter(
            fmt="Log Level [%(level)s] | %(timestamp)s - %(name)s %(message)s %(user_id)s %(action)s %(extra)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"}
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
            file_handler = FileJSONHandler(file_path, 'log', maxBytes=5_000_000, backupCount=3)
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
        return logging.LoggerAdapter(self.logger, context or {})
