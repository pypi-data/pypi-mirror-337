import os
import socket
from pythonjsonlogger.json import JsonFormatter
from pythonjsonlogger.core import RESERVED_ATTRS

JSON_FORMATTER_CONFIG = {
    'fmt': '{message}{asctime}{levelno}',
    'style': '{',
    'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
    'rename_fields': {
        'asctime': 'timestamp',
        'message': 'msg',
        'levelno': 'level'
    },
    'reserved_attrs': RESERVED_ATTRS+['color_message'],
    'static_fields': {
        'name': os.getenv('APP_NAME'),
        'pid': os.getpid(),
        'hostname': socket.gethostname()
    }
}

formatter = JsonFormatter(
    JSON_FORMATTER_CONFIG['fmt'],
    style=JSON_FORMATTER_CONFIG['style'],
    static_fields=JSON_FORMATTER_CONFIG['static_fields'],
    rename_fields=JSON_FORMATTER_CONFIG['rename_fields'],
    reserved_attrs=JSON_FORMATTER_CONFIG['reserved_attrs'],
    datefmt=JSON_FORMATTER_CONFIG['datefmt']
)
