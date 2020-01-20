# app/views/weapons.py

import flask_restplus
from functools import wraps

from app.helpers import search, get_as_object
from app.models import WeaponData
from app.constants import NS, API, cache
from orm import Select


#
# Helpers
#

def get_categories(item_type):
    """Get all categories within type """
    symbol = '>' if item_type.lower() == 'ranged' else '<='
    data = Select('type', 'weapon_categories', where=f'id {symbol} 11').all()
    response = set(  # reject duplicates
        item['type']
        for item in data
    )
    return list(response)


def get_category_ids(category):
    """List of sub-category ids within category """
    if category:
        where = f"type='{category}'"
    data = Select('id', 'weapon_categories', where=where).all()
    return [
        item['id']
        for item in data
    ]


def limit_weapon_categories(function):
    @wraps(function)
    def limit(*args, **kwargs):
        category = kwargs['category']
        if category == "all":
            kwargs['category'] = False
            return function(*args, **kwargs)

        # If category provided, parse and format it
        category = category.replace('_', ' ')
        category = category.replace(' weapons', '')
        if category.endswith('s'):
            category = category[:-1]
        if category == "basic" or category == "advanced":
            category = f"{category} melee"

        # Check for category in known categories

        item_type = kwargs.get('item_type', 'melee')
        if category not in get_categories(item_type):
            return {"Error": (
                        f"{category} is not a known {item_type} category. "
                        f"Try this: {NS.weapon._path}/categories/{item_type}/"
                    )}, 404

        # If found, return formatted category name
        kwargs['category'] = category
        return function(*args, **kwargs)
    return limit


def limit_weapon_types(function):
    @wraps(function)
    def limit(*args, **kwargs):
        """Decorator to check 'item_type' input """
        item_type = kwargs['item_type']
        if item_type.lower() == "ranged" or item_type.lower() == "melee":
            return function(*args, **kwargs)  # return normal function
        return {"Error": "Weapon type may be 'ranged' or 'melee'"}, 404
    return limit


def where_category_is(category):
    """Instead of matching exact category id, check list of ids """
    category_ids = get_category_ids(category)
    first = True
    for category_id in category_ids:
        if first:  # don't put a comma at the beginning
            ids = f"'{category_id}'"
            first = False
        else:  # all subsequent ids should prepend a comma
            ids = f"{ids},'{category_id}'"
    return f"category IN({ids})"


#
# Routes
#

@NS.weapon.route('/<string:item_type>/search/<string:search_term>/')
@API.param("item_type", "'melee' or 'ranged'")
@API.param("search_term", "Example: 'flame'")
class SearchWeapons(flask_restplus.Resource):
    @limit_weapon_types
    @cache.cached()
    def get(self, item_type, search_term):
        """Search for weapon by type and name"""
        return search(f"{item_type}_weapons", search_term, model=WeaponData)


@NS.weapon.route('/<string:item_type>/raw/')
@API.param("item_type", "'melee' or 'ranged'")
class GetWeaponsRaw(flask_restplus.Resource):
    @limit_weapon_types
    @cache.cached()
    def get(self, item_type):
        """All entries for specified type, unformatted"""
        data = Select('*', f'{item_type}_weapons').all()
        if "Error" in str(data):
            return data, 500
        return data


@NS.weapon.route('/<string:item_type>/')
@API.param("item_type", "'melee' or 'ranged'")
class GetWeapons(flask_restplus.Resource):
    @cache.cached()
    @limit_weapon_types
    def get(self, item_type):
        """All entries for specified type"""
        return get_as_object(f"{item_type}_weapons", WeaponData)


@NS.weapon.route('/melee/hands/<int:hands>/')
@API.param("hands", "'1' or '2'")
class GetWeaponsByHandCount(flask_restplus.Resource):
    @cache.cached()
    def get(self, hands):
        """All melee weapons, by hand count"""
        if hands != 1 and hands != 2:  # error for all other input
            return {"Error": "Weapons can be either 1 or 2 handed"}
        where = f"hands = '{hands}'"
        return get_as_object("melee_weapons", WeaponData, where=where)


@NS.weapon.route('/<string:item_type>/categories/')
@API.param("item_type", "'melee' or 'ranged'")
class GetWeaponCategories(flask_restplus.Resource):
    @limit_weapon_types
    @cache.cached()
    def get(self, item_type):
        """List of categories for the specified type"""
        return get_categories(item_type)


@NS.weapon.route('/<string:item_type>/category/<string:category>/')
@API.param("item_type", "'melee' or 'ranged'")
@API.param("category", f"Reference: {NS.weapon._path}/categories/<item_type>")
class GetWeaponsByCategory(flask_restplus.Resource):
    @limit_weapon_categories
    @cache.cached()
    def get(self, item_type, category):
        """All entries for specified type and category """
        where = where_category_is(category)
        return get_as_object(
            f"{item_type}_weapons",
            WeaponData,
            where=where,
            category=category)


@NS.weapon.route('/melee/category/<string:category>/hands/<int:hands>/')
@API.param("category", f"For examples: {NS.weapon._path}/categories/melee")
@API.param("hands", "'1' or '2'")
class GetWeaponFromCategoryByHandCount(flask_restplus.Resource):
    @limit_weapon_categories
    @cache.cached()
    def get(self, category, hands):
        """Melee weapons within category, by hands required"""
        where = where_category_is(category)
        where = f"{where} AND hands = '{hands}'"
        return get_as_object("melee_weapons", WeaponData, where=where)


@NS.weapon.route('/<string:item_type>/<string:item_name>/')
@API.param("item_type", "'melee' or 'ranged'")
@API.param("item_name", "Example: bow")
class GetWeapon(flask_restplus.Resource):
    @limit_weapon_types
    @cache.cached()
    def get(self, item_type, item_name):
        """Get weapon by type and name"""
        weapon = WeaponData(
                name=item_name, table=f"{item_type}_weapons"
            )
        if not hasattr(weapon, 'level') or hasattr(weapon, 'error'):
            return {"Error": f"'{item_name}' not found in {item_type} weapons."
                    f" Try this: {NS.weapon._path}/{item_type}/search/"
                    f"{item_name.replace(' ', '%20')}"
                    }, 404
        return weapon.associative_data()
