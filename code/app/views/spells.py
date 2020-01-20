# app/views/spells.py

import flask_restplus

from app.helpers import search, data_list_to_model_dict
from app.models import SpellData
from app.constants import APP, NS, API, cache
from orm import Select


#
# Routes
#

@NS.spells.route('/search/<string:search_term>/')
@API.param("search_term", "Example: 'knock'")
class SearchSpells(flask_restplus.Resource):
    @cache.cached()
    def get(self, search_term):
        """Search for spell by name"""
        return search("spells", search_term, model=SpellData)


@NS.spells.route('/mystic/all/')
class MysticSpells(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Show all mystic spells"""
        data = Select('*', 'spells', where="mystic_level IS NOT NULL").all()
        return data_list_to_model_dict(data, SpellData)


@NS.spells.route('/technomancer/all/')
class TechnomancerSpells(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Show all technomancer spells"""
        where = "technomancer_level IS NOT NULL"
        data = Select('*', 'spells', where=where).all()
        return data_list_to_model_dict(data, SpellData)


@NS.spells.route('/technomancer/<int:level>/')
@API.param("level", "Max Spell Level")
class TechnomancerSpellsByLevel(flask_restplus.Resource):
    @cache.cached()
    def get(self, level):
        """Show all technomancer spells under a specific level"""
        where = f"technomancer_level <= {level}"
        data = Select('*', 'spells', where=where).all()
        return data_list_to_model_dict(data, SpellData)


@NS.spells.route('/mystic/<int:level>/')
@API.param("level", "Max Spell Level")
class MysticSpellsByLevel(flask_restplus.Resource):
    @cache.cached()
    def get(self, level):
        """Show all mystic spells under a specific level"""
        where = f"mystic_level <= {level}"
        data = Select('*', 'spells', where=where).all()
        return data_list_to_model_dict(data, SpellData)


@NS.spells.route('/<string:spell_name>/')
class GetSpellByName(flask_restplus.Resource):
    @cache.cached()
    def get(self, spell_name):
        """Specific spell, by name"""
        spell = SpellData(name=spell_name)
        if hasattr(spell, 'error'):
            APP.logger.info(f"Query error for {spell_name}: {spell.error}")
            return {"Error": f"Spell {spell_name} not found."
                    f" Try this: {NS.spells._path}/search/"
                    f"{spell_name.replace(' ', '%20')}"
                    }, 404
        return spell.associative_data()
