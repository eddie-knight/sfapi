# app/views/abilities.py

import flask_restplus

from orm import Select
from app.constants import API, NS, cache


#
# Routes
#

@NS.abilities.route('/')
class GetAbilityList(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Get all abilities data """
        return Select('*', "abilities").all()


@NS.abilities.route('/<string:ability>/')
@API.param("ability", "Example: 'dexterity' or 'dex'")
class GetAbility(flask_restplus.Resource):
    @cache.cached()
    def get(self, ability):
        """Get ability by name or shorthand """
        where = f"name = '{ability}' OR shorthand = '{ability}'"
        return Select('*', "abilities", where=where).all()
