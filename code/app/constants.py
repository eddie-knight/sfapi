# app/constants.py

from flask import Flask
from flask_caching import Cache
import flask_restplus
from .namespaces import Namespaces
#
# Flask / Swagger Elements
#

APP = Flask(__name__)
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
