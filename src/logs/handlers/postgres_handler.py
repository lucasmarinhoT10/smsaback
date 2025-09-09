import json
import logging
from datetime import datetime

import psycopg2


class PostgresHandler(logging.Handler):
    """
    PostgresHandler é uma classe personalizada que herda de logging.Handler e permite registrar logs diretamente em uma tabela do PostgreSQL.

    - No construtor (__init__), recebe a string de conexão (dsn), o nome do banco de dados (database) e o nome da tabela (table) onde os logs serão armazenados.
    - Garante que o banco de dados e a tabela existam, criando-os se necessário.
    - Mantém uma conexão persistente com o banco de dados para inserção dos logs.

    Métodos:
    - _ensure_database: Verifica se o banco de dados de destino existe; caso não exista, cria o banco.
    - _ensure_table: Garante que a tabela de logs exista no banco, criando-a se necessário.
    - emit: Método chamado automaticamente pelo sistema de logging do Python para cada registro de log. Formata o registro, converte para dicionário e insere na tabela do PostgreSQL.
    """

    def __init__(self, dsn: str, database: str, table: str = "logs"):
        """
        Inicializa o handler, garantindo a existência do banco e da tabela.
        Parâmetros:
            dsn (str): String de conexão base para o PostgreSQL.
            database (str): Nome do banco de dados onde os logs serão armazenados.
            table (str): Nome da tabela de logs (padrão: "logs").
        """
        super().__init__()
        self.dsn = dsn
        self.database = database
        self.table = table
        self._ensure_database()
        self.conn = psycopg2.connect(dsn, database=database)
        self.cursor = self.conn.cursor()
        self._ensure_table()

    def _ensure_database(self):
        """
        Garante que o banco de dados de destino exista.
        Conecta-se ao banco 'postgres' padrão, verifica se o banco desejado existe e, se não existir, cria o banco.
        """
        conn = psycopg2.connect(self.dsn, database="postgres")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.database,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE "{self.database}"')
        cursor.close()
        conn.close()

    def _ensure_table(self):
        """
        Garante que a tabela de logs exista no banco de dados.
        Cria a tabela caso ela ainda não exista, com colunas para timestamp, nível, nome, usuário, ação, mensagem e dados extras em JSON.
        """
        self.cursor.execute(
            f"""
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
        """
        )
        self.conn.commit()

    def emit(self, record):
        """
        Insere um registro de log na tabela do PostgreSQL.
        Formata o registro de log, converte para dicionário e insere os campos na tabela.
        Em caso de erro, imprime uma mensagem de erro no console.
        """
        try:
            log_entry = self.format(record)
            log_data = json.loads(log_entry)

            self.cursor.execute(
                f"""
                INSERT INTO {self.table} (timestamp, level, name, user_id, action, message, extra)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    datetime.fromisoformat(log_data["timestamp"]),
                    log_data["level"],
                    log_data["name"],
                    log_data.get("user_id"),
                    log_data.get("action"),
                    log_data["message"],
                    json.dumps(log_data.get("extra", {})),
                ),
            )
            self.conn.commit()
        except Exception as e:
            print(f"[PostgresHandler ERROR] {e}")
