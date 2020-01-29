import os
import logging

from flask import Flask
import loguru


basedir = os.path.abspath(os.path.dirname(__file__))


class _InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = loguru.logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


class _Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'SUPER-SECRET')
    LOGFILE = "log.log"


class _DevelopmentConfig(_Config):
    DEBUG = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'DEBUG'


class _ProductionConfig(_Config):
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'


__config = {
    'development': _DevelopmentConfig,
    'production': _ProductionConfig,
    'default': _DevelopmentConfig
}


def setup(config_name):
    app = Flask(__name__)
    app.config.from_object(__config[config_name])

    loguru.logger.start(app.config['LOGFILE'], level=app.config['LOG_LEVEL'], format="{time} {level} {message}",
                 backtrace=app.config['LOG_BACKTRACE'], rotation='25 MB')
    
    # replace default handler with loguru handler
    app.logger.addHandler(_InterceptHandler())

    return app