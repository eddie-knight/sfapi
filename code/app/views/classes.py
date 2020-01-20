# app/views/classes.py

import flask_restplus
from functools import wraps

from orm import Select
from app.models import ClassData
from app.constants import NS, API, cache


#
# Helpers
#

def limit_existing_classes(function):
    @wraps(function)
    def limit(*args, **kwargs):
        # Check for class_name in the database first
        class_names = [
            entry['name']
            for entry in Select('name', 'classes').all()
        ]
        name = kwargs["class_name"]
        if name.capitalize() not in class_names:
            return {"Error": f"Class '{name}' not found in classes'"}, 404
        return function(*args, **kwargs)
    return limit


#
# Routes
#

@NS.classes.route('/<string:class_name>/')
@API.param("class_name", "Example: 'mystic'")
class GetFormattedClassData(flask_restplus.Resource):
    @limit_existing_classes
    @cache.cached()
    def get(self, class_name):
        """Formatted class data"""
        class_data = ClassData(name=class_name)
        return class_data.associative_data()


@NS.classes.route('/<string:class_name>/<string:attribute>/')
@API.param("class_name", "Example: 'mystic'")
@API.param("attribute", f"Any attribute from {NS.classes._path}/<class_name>")
class GetFormattedClassProgressionData(flask_restplus.Resource):
    @limit_existing_classes
    @cache.cached()
    def get(self, class_name, attribute):
        """Individual attribute data from specified class"""
        class_data = ClassData(name=class_name)
        return getattr(class_data, attribute)
