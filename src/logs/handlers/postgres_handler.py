import logging
import json
import psycopg2
from datetime import datetime

class PostgresHandler(logging.Handler):
    def __init__(self, dsn: str, database: str, table: str = "logs"):
        super().__init__()
        self.dsn = dsn
        self.database = database
        self.table = table
        self._ensure_database()
        self.conn = psycopg2.connect(dsn, database=database)
        self.cursor = self.conn.cursor()
        self._ensure_table()

    def _ensure_database(self):
        # Conecta ao banco 'postgres' para verificar/criar o banco de destino
        conn = psycopg2.connect(self.dsn, database='postgres')
        conn.autocommit = True  # Necessário para CREATE DATABASE fora de transação
        cursor = conn.cursor()
        # O PostgreSQL não suporta "CREATE DATABASE IF NOT EXISTS" diretamente.
        # Portanto, precisamos checar se o banco existe antes de criar.
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.database,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE "{self.database}"')
        cursor.close()
        conn.close()

    def _ensure_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                level VARCHAR(20),
                name VARCHAR(100),
                user_id VARCHAR(50),
                action VARCHAR(100),
                message TEXT,
                extra JSONB
            );
        """)
        self.conn.commit()

    def emit(self, record):
        try:
            log_entry = self.format(record)
            log_data = json.loads(log_entry)

            self.cursor.execute(f"""
                INSERT INTO {self.table} (timestamp, level, name, user_id, action, message, extra)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                datetime.fromisoformat(log_data["timestamp"]),
                log_data["level"],
                log_data["name"],
                log_data.get("user_id"),
                log_data.get("action"),
                log_data["message"],
                json.dumps(log_data.get("extra", {}))
            ))
            self.conn.commit()
        except Exception as e:
            print(f"[PostgresHandler ERROR] {e}")
