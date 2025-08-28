from pythonjsonlogger import jsonlogger

class FileJsonFormatter(jsonlogger.JsonFormatter):
    """
    FileJsonFormatter é uma classe personalizada que herda de JsonFormatter da biblioteca pythonjsonlogger.
    Seu objetivo é garantir que os logs gravados em arquivo estejam sempre no formato JSON padronizado,
    preenchendo campos essenciais como timestamp, nível do log e nome do logger, mesmo que não estejam presentes originalmente no registro.

    Essa classe é utilizada principalmente por handlers de arquivo, como o FileWriteHandler, para garantir
    que cada linha do arquivo de log contenha todas as informações relevantes de forma estruturada.
    """

    def add_fields(self, log_record, record, message_dict):
        """
        O método add_fields é chamado durante a formatação do log para adicionar ou corrigir campos no dicionário final do log.
        Ele garante que os campos 'timestamp', 'level' e 'name' estejam sempre presentes no registro JSON.
        Caso algum desses campos não exista, ele é preenchido com o valor apropriado extraído do objeto record.

        Parâmetros:
            log_record (dict): Dicionário que representa o registro de log final.
            record (LogRecord): Objeto LogRecord original do Python.
            message_dict (dict): Dicionário com os campos extras passados no log.
        """
        super().add_fields(log_record, record, message_dict)

        # Corrige timestamp
        if not log_record.get("timestamp"):
            log_record["timestamp"] = self.formatTime(record, "%Y-%m-%dT%H:%M:%S")

        # Corrige nível
        if not log_record.get("level"):
            log_record["level"] = record.levelname

        # nome do logger
        if not log_record.get("name"):
            log_record["name"] = record.name