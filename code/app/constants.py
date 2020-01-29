# app/constants.py
import os

from flask_caching import Cache
import flask_restplus

import config
from app.namespaces import Namespaces
#
# Flask / Swagger Elements
#

environment = os.getenv("environment", "development")
APP = config.setup(environment)
cache = Cache(config={
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 86400
    }
)
API = flask_restplus.Api(
    APP,
    version="1.0",
    title="Starfinder Fan API",
    description="A Starfinder database built by fans for fans"
)
NS = Namespaces(API)
