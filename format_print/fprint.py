from . import color
from datetime import datetime

col = color.Color()


def logger(identifier, value, mode="info") -> str:
    """
    Simple class to print logs
    :param identifier: Identifier KEY
    :param value: Value assigned to identifier KEY
    :param mode: Specify whether the message is an "error", a "success" or "normal"
    :return: str
    """

    assert mode in ["info", "success", "error"], 'Mode must be "error", "success" or "info".'

    time = datetime.now().strftime("%H:%M:%S")

    if mode.lower() == 'info':
        log = f"{time} [{col.fore_color('#', 'YELLOW')}] {col.fore_color(str(identifier), 'YELLOW')}: {value}"

    elif mode.lower() == 'error':
        log = f"{time} [{col.fore_color('!', 'RED')}] {col.fore_color(str(identifier), 'RED')}: " \
              f"{col.fore_color(str(value), 'RED')}"

    elif mode.lower() == 'success':
        log = f"{time} [{col.fore_color('$', 'GREEN')}] {col.fore_color(str(identifier), 'GREEN')}: {value}"

    print(log)
    return log
