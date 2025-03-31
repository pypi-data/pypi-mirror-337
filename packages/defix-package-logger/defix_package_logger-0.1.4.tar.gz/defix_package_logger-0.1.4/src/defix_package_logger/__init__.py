import os
import socket
from typing import Dict
import logging
from pythonjsonlogger.json import JsonFormatter

logger: logging.Logger = None


def initialize(opts: Dict):
    global logger

    if logger is not None:
        return

    if opts['name'] is None or len(opts['name']) < 1:
        raise Exception('Service name is empty')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler()
    formatter = JsonFormatter(
        "{message}{asctime}{levelno}",
        style="{",
        static_fields={'name': opts['name'], 'pid': os.getpid(
        ), 'hostname': socket.gethostname()},
        rename_fields={'asctime': 'timestamp',
                       'message': 'msg', 'levelno': 'level'},
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )
    logHandler.setFormatter(formatter)

    logger.addHandler(logHandler)


__all__ = ['initialize', 'logger']
