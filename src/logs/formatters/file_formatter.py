from pythonjsonlogger import jsonlogger

class FileJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
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