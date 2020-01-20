# app/views/races.py

import flask_restplus

from app.models import BasicData
from app.helpers import data_list_to_model_dict
from app.constants import NS, cache
from orm import Select


#
# Routes
#

@NS.races.route('/all')
class AllRaces(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Data for all races"""
        data = Select('*', 'races').all()
        return data_list_to_model_dict(data, BasicData)
