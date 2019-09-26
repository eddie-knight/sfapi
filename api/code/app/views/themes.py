# app/views/themes.py

import flask_restplus

from app.models import ThemeData
from app.helpers import data_list_to_model_dict
from app.constants import NS, cache
from orm import Select


#
# Routes
#

@NS.themes.route('/all')
class AllThemes(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Data for all themes"""
        data = Select('*', 'themes').all()
        return data_list_to_model_dict(data, ThemeData)


@NS.themes.route('/<string:theme_name>')
class GetTheme(flask_restplus.Resource):
    @cache.cached()
    def get(self, theme_name):
        """Data for a specified theme"""
        theme = ThemeData(table='themes', name=theme_name)
        if hasattr(theme, 'error'):
            return {"Error": f"'{theme_name}' not found in themes"}
        return theme.associative_data()


@NS.themes.route('/<string:theme_name>/<string:attribute>')
class GetThemeAttribute(flask_restplus.Resource):
    @cache.cached()
    def get(self, theme_name, attribute):
        """Attribute for a specified theme"""
        theme = ThemeData(table='themes', name=theme_name)
        if hasattr(theme, 'error'):
            return {"Error": f"'{theme_name}' not found in themes"}
        return theme.data()[attribute]
