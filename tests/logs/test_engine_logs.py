import logging
import os
import unittest
from logging import StreamHandler
from unittest.mock import patch

from src.logs.engine_logs import EngineLogs


class TestEngineLogs(unittest.TestCase):
    def setUp(self):
        """Executa antes de cada teste, limpando variáveis de ambiente."""
        for key in list(os.environ.keys()):
            del os.environ[key]

    @patch.dict(os.environ, {"ENVIRONMENT": "test", "LOG_LEVEL": "DEBUG"})
    def test_logger_level_and_name(self):
        engine_logs = EngineLogs()
        logger = engine_logs.get_logger()
        self.assertEqual(logger.logger.name, "test")
        self.assertEqual(logger.logger.level, logging.DEBUG)

    @patch.dict(os.environ, {"LOG_CONSOLE": "true"})
    def test_add_console_handler(self):
        engine_logs = EngineLogs()
        # Verifica se algum handler é do tipo StreamHandler (console)
        self.assertTrue(
            any(isinstance(h, StreamHandler) for h in engine_logs.logger.handlers)
        )

    @patch.dict(os.environ, {"LOG_FILE": "true", "LOG_FILE_PATH": "test/"})
    @patch("src.logs.engine_logs.FileWriteHandler")
    def test_adiciona_file_handler(self, mock_file_handler):
        engine_logs = EngineLogs()
        self.assertTrue(
            any(
                isinstance(h, mock_file_handler.return_value.__class__)
                for h in engine_logs.logger.handlers
            )
        )
        mock_file_handler.assert_called_with(
            "test/", "log", maxBytes=5_000_000, backupCount=3
        )

    @patch.dict(os.environ, {})
    def test_get_logger_adapter_context(self):
        engine_logs = EngineLogs()
        contexto = {"user_id": "123", "action": "login"}
        logger = engine_logs.get_logger(contexto)
        self.assertIsInstance(logger, logging.LoggerAdapter)
        self.assertEqual(logger.extra, contexto)

    @patch.dict(os.environ, {})
    def test_get_logger_adapter_context_none(self):
        engine_logs = EngineLogs()
        logger = engine_logs.get_logger()
        self.assertIsInstance(logger, logging.LoggerAdapter)
        self.assertEqual(logger.extra, {})

    # @patch.dict(os.environ, {"LOG_POSTGRES": "true", "POSTGRES_URI": "postgresql://user:pass@localhost/", "POSTGRES_DATABASE": "testsdb"})
    # @patch("src.logs.engine_logs.PostgresHandler")
    # def test_adiciona_postgres_handler(self, mock_pg_handler):
    #     engine_logs = EngineLogs()
    #     # Verifica se algum handler é exatamente a instância mockada
    #     self.assertTrue(
    #         any(h is mock_pg_handler.return_value for h in engine_logs.logger.handlers)
    #     )
    #     mock_pg_handler.assert_called_with("postgresql://user:pass@localhost/", "testsdb")

    # @patch.dict(os.environ, {
    #     "LOG_MONGO": "true",
    #     "MONGO_URI": "mongodb://user:pass@localhost:27017/",
    #     "MONGO_DB": "testsdb",
    #     "MONGO_COLLECTION": "logs"
    # })
    # @patch("src.logs.engine_logs.MongoHandler")
    # def test_adiciona_mongo_handler(self, mock_mongo_handler):
    #     engine_logs = EngineLogs()
    #     # Verifica se algum handler é exatamente a instância mockada
    #     self.assertTrue(
    #         any(h is mock_mongo_handler.return_value for h in engine_logs.logger.handlers)
    #     )
    #     mock_mongo_handler.assert_called_with("mongodb://user:pass@localhost:27017/", "testsdb", "logs")


if __name__ == "__main__":
    unittest.main()
