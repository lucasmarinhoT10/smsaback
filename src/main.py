from logs.engine_logs import EngineLogs

if __name__ == "__main__":
    motor = EngineLogs()
    log = motor.get_logger({"user_id": "u123", "action": "login"})

    log.info("Usuário logado com sucesso", extra={"extra": {"ip": "127.0.0.1"}})
    log.warning("Tentativa suspeita de login", extra={"extra": {"ip": "10.0.0.99"}})
    log.error("Erro ao buscar dados", extra={"extra": {"query": "SELECT *"}})
    log.debug("O usuário foi adicionado na base de dados", extra={"extra": {"query": "SELECT *"}})
