import json
import logging

from pymongo import MongoClient


class MongoHandler(logging.Handler):
    """
    MongoHandler é uma classe personalizada que herda de logging.Handler e serve para registrar logs diretamente em uma coleção do MongoDB.

    - No construtor (__init__), recebe a URI de conexão do MongoDB, o nome do banco de dados (db) e o nome da coleção (collection) onde os logs serão armazenados.
    - Cria uma conexão com o MongoDB e define a coleção alvo para inserção dos logs.

    O método emit é chamado automaticamente pelo sistema de logging do Python sempre que um novo registro de log precisa ser processado por este handler.

    - O emit recebe um objeto record (registro de log), formata esse registro usando o formatter associado ao handler (transformando-o em string JSON), converte para dicionário Python e insere o documento na coleção do MongoDB.
    - Caso ocorra qualquer exceção durante o processo, imprime uma mensagem de erro no console.
    """

    def __init__(self, uri: str, db: str = "logsdb", collection: str = "logs"):
        super().__init__()
        self.client = MongoClient(uri)
        self.collection = self.client[db][collection]

    def emit(self, record):
        """
        O método emit é responsável por receber o registro de log (record), formatá-lo em JSON e inserir o resultado como um documento na coleção do MongoDB.
        Caso ocorra algum erro durante a inserção, uma mensagem de erro é impressa no console.
        """
        try:
            log_entry = self.format(record)
            log_data = json.loads(log_entry)
            self.collection.insert_one(log_data)
        except Exception as e:
            print(f"[MongoHandler ERROR] {e}")
