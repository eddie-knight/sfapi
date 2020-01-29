# run.py

from app.constants import APP, cache
import orm
from loguru import logger


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # logging properties are defined in config.py
    logger.start(app.config['LOGFILE'], level=app.config['LOG_LEVEL'], format="{time} {level} {message}",
                 backtrace=app.config['LOG_BACKTRACE'], rotation='25 MB')
    
    #register loguru as handler
    app.logger.addHandler(InterceptHandler())

    # register Blueprints here
    # ...

    return app


if __name__ == '__main__':
    orm.setup()
    cache.init_app(APP)
    APP.run(debug=True, host='0.0.0.0')  # Do not write code after this point
