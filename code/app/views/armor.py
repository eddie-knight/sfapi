# app/views/armor.py

import flask_restplus
from functools import wraps

from app.helpers import search, get_as_object
from app.models import ArmorData
from app.constants import NS, API, cache


#
# Helpers
#

def limit_armor_types(function):
    @wraps(function)
    def limit(*args, **kwargs):
        armor_type = kwargs['item_type'].lower()
        if armor_type == "light" or armor_type == "heavy":
            return function(*args, **kwargs)
        return {"Error": "Armor Type can be 'heavy' or 'light'"}, 404
    return limit


#
# Routes
#

@NS.armor.route('/<string:item_type>/')
@API.param("item_type", "'light' or 'heavy'")
class GetArmorByType(flask_restplus.Resource):
    @limit_armor_types
    @cache.cached()
    def get(self, item_type):
        """All light or heavy armor data"""
        armor_type_id = 0 if item_type == "light" else 1
        where = f"type={armor_type_id}"
        return get_as_object("armor", ArmorData, where=where)


@NS.armor.route('/<string:item_type>/<string:entry_name>/')
@API.param("item_type", "'light' or 'heavy'")
@API.param("entry_name", "Example: 'Second skin'")
class GetArmorEntry(flask_restplus.Resource):
    @limit_armor_types
    @cache.cached()
    def get(self, item_type, entry_name):
        """Data for one armor item, by type and name"""
        armor = ArmorData(name=entry_name)
        if not hasattr(armor, 'level'):
            return {"Error": f"'{entry_name}' not found in {item_type} armor. "
                    f"Try this: '{NS.armor._path}/{item_type}/search/"
                    f"{entry_name.replace(' ', '%20')}'"
                    }, 404
        return armor.associative_data()


@NS.armor.route('/<string:item_type>/search/<string:search_term>/')
@API.param("item_type", "'light' or 'heavy'")
@API.param("search_term", "Example: 'skin'")
class SearchArmor(flask_restplus.Resource):
    @cache.cached()
    @limit_armor_types
    def get(self, item_type, search_term):
        """Search for armor by type"""
        armor_type_id = 0 if item_type == "light" else 1
        where = f"type={armor_type_id}"
        return search(f"armor", search_term, where=where, model=ArmorData)
