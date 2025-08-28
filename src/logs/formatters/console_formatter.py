import logging
import os
from datetime import datetime

COLORS = {
    "timestamp": "\033[38;5;40m",  # verde escuro para o timestamp
    "record_section": "\033[38;5;37m",  # turquesa
    "DEBUG": "\033[38;5;27m",      # azul/ciano
    "INFO": "\033[37m",       # branco
    "WARNING": "\033[33m",    # amarelo
    "ERROR": "\033[31m",      # vermelho
    "CRITICAL": "\033[1;31m", # vermelho forte
    "RESET": "\033[0m" # reset
}

class ConsoleFormatter(logging.Formatter):
    """
    ConsoleFormatter é uma classe personalizada que herda de logging.Formatter e tem como objetivo formatar as mensagens de log exibidas no console de forma mais legível e colorida.

    Ela utiliza códigos de cores ANSI para destacar diferentes partes do log, como o timestamp, o nível do log (INFO, WARNING, ERROR, etc.), o local do código onde o log foi gerado (nome do logger, função e linha), além da própria mensagem.

    O método principal é o `format`, que monta a string final do log, aplicando as cores e o layout desejado. Caso a mensagem contenha múltiplas linhas, cada linha é formatada separadamente para manter a legibilidade. Se houver exceção associada ao log, ela também é formatada e destacada.

    Essa formatação facilita a identificação rápida de informações importantes no terminal, tornando o processo de depuração e monitoramento mais eficiente.
    """
    def format(self, record):
        level = record.levelname

        color = COLORS.get(level, COLORS["RESET"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")

        timestamp_str = f"{COLORS['timestamp']}{timestamp}{COLORS['RESET']}"

        record_section = (
            f"{COLORS['record_section']}"
            f"{record.name}.{record.funcName}:{record.lineno}"
            f"{COLORS['RESET']}"
        )
        header = f"{timestamp_str} | {color}{level:<8}{COLORS['RESET']} | {record_section} -"

        message = record.getMessage()

        if "\n" in message:
            formatted_msg = "\n  " + "\n  ".join(
                f"{color}{linha}{COLORS['RESET']}" for linha in message.splitlines()
            )
        else:
            formatted_msg = f" {color}{message}{COLORS['RESET']}"

        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            formatted_msg += f"\n{COLORS['WARNING']}{exc_text}{COLORS['RESET']}"

        return f"{header}{formatted_msg}"