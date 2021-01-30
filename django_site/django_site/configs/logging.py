import logging
import logging.config
import os

from ..settings import BASE_DIR


log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {                            # 定义一个日志的格式器
            'format': '{asctime} {levelname:5} {threadName:15}  {message}',
            'datefmt': '%Y/%m/%d %H:%M:%S',
            'style': '{'

        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {                            # 定义一个日志的处理器
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',   # 将日志输出到终端
            'filters': ['require_debug_true'],  # 当 Django 处于调试模式时，才记录日志
            'formatter': 'verbose',
        },
        'logfile': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 将日志输出到文件，并按时间自动翻转文件
            'filename': os.path.join(log_dir, 'django.log'),
            'encoding': 'utf-8',
            'utc': False,
            'when': 'D',
            'interval': 1,
            'backupCount': 15,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',    # 记录 INFO 级别以上的日志
            'propagate': True,
        }
    }
}

logging.config.dictConfig(LOGGING)
logging.addLevelName(logging.WARNING, 'WARN')
logging.addLevelName(logging.CRITICAL, 'FATAL')
logger = logging.getLogger('django')

