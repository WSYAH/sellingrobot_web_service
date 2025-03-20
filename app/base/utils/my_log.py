# -*- coding: utf-8 -*-
import copy
import logging
import logging.config
import logging.handlers
import os
from enum import unique, Enum

from app.base import data


@unique
class DirMode(Enum):
    CONFIG = 0
    PACKAGE = 1
    DEFAULT_SETTING = {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "formatter": "simple",
        "when": "midnight",
        "interval": 1,
        "backupCount": 6,
        "encoding": 'utf-8'
    }


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "log_dir": "logs/",
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(name)s] [%(module)s#%(funcName)s] [%(levelname)s]- %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "debug": {**DirMode.DEFAULT_SETTING.value, **{
            "level": "DEBUG",
            "filename": "debug.log"
        }},
        "info": {**DirMode.DEFAULT_SETTING.value, **{
            "level": "INFO",
            "filename": "info.log",
        }},
        "warn": {**DirMode.DEFAULT_SETTING.value, **{
            "level": "WARN",
            "filename": "warn.log",
        }},
        "error": {**DirMode.DEFAULT_SETTING.value, **{
            "level": "ERROR",
            "filename": "error.log",
        }}
    },

    "root": {
        'handlers': ['debug', "info", "warn", "error"],
        'level': "DEBUG",
        'propagate': False
    }
}


def get_filter(level):
    if level == logging.DEBUG:
        return lambda record: record.levelno < logging.INFO
    elif level == logging.INFO:
        return lambda record: record.levelno < logging.WARN
    elif level == logging.WARN:
        return lambda record: record.levelno < logging.ERROR
    else:
        return lambda record: record.levelno <= logging.FATAL


def adjust_config(logging_config, dir_mode=DirMode.CONFIG):
    # 使用配置目录
    if dir_mode == DirMode.CONFIG:
        dir_name = logging_config['log_dir']
    else:
        # currentdir = os.path.dirname(__file__).replace('\\', '/')
        dir_name = data['log_path']
        if dir_name[-1] != '/':
            dir_name += '/'

    handlers = logging_config.get('handlers')
    for handler_name, handler_config in handlers.items():
        filename = handler_config.get('filename', None)
        if filename is None:
            continue
        if dir_name is not None:
            if not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name)
                except Exception as e:
                    print(e)
            handler_config['filename'] = dir_name + filename
    return logging_config


def get_logger(name=None):
    #  拷贝配置字典
    logging_config = copy.deepcopy(LOGGING_CONFIG)
    # 调整配置内容
    adjust_config(logging_config, DirMode.PACKAGE)
    # 使用调整后配置生成logger
    logging.config.dictConfig(logging_config)
    res_logger = logging.getLogger(name)
    for handler in res_logger.root.handlers:
        if handler.name == 'console':
            continue
        log_filter = logging.Filter()
        log_filter.filter = get_filter(handler.level)
        handler.addFilter(log_filter)
    return res_logger
