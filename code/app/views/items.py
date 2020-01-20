# app/views/items.py

import flask_restplus
from functools import wraps

from app.helpers import search
from app.models import BasicData
from app.constants import APP, NS, API, cache
from app.views.searches import search_by_price
from orm import Select

ITEMS_TABLES = [
                'ammunition',
                'armor_upgrades',
                'augmentations',
                'equipment',
                'personal_upgrades',
                'solarian_crystals',
                'tech_items',
                'weapon_fusions'
                ]


#
# Helpers
#

def limit_item_types(function):
    @wraps(function)
    def limit(*args, **kwargs):
        item_type = kwargs['item_type'].lower()
        if item_type in ITEMS_TABLES:
            return function(*args, **kwargs)
        return {"Error": (f"{item_type} not a known item type. "
                          f"See {NS.items._path}/types for available types.")
                }, 404
    return limit


def associative_data_dict(data_list, table):
    if "Error" in data_list:
        APP.logger.warning(data_list)
    APP.logger.info(f"Results in query: {len(data_list)}")
    output = {}
    for item in data_list:
        data = BasicData(table, data=item).data()
        name = data.pop('name')
        if 'model' in data and data['model'] is not None:
            name = f"{name}, {data.pop('model')}"
        output[name] = data
    return output


#
# Routes
#

@NS.items.route('/types')
class ItemTypes(flask_restplus.Resource):
    def get(self):
        """List of types that can be retrieved """
        return ITEMS_TABLES


@NS.items.route('/all')
class AllItems(flask_restplus.Resource):
    def get(self):
        """Get all items, sorted by type"""
        full_data = {}
        for table in ITEMS_TABLES:
            data = Select('*', table).all()
            data_dict = associative_data_dict(data, table)
            full_data[table.capitalize()] = data_dict
        return full_data


@NS.items.route('/<string:item_type>')
@API.param('item_type', f"See {NS.items._path}/types for examples")
class AllItemsByType(flask_restplus.Resource):
    @limit_item_types
    def get(self, item_type):
        """Get all items for type"""
        data = Select('*', item_type).all()
        return associative_data_dict(data, item_type)


@NS.items.route('/<string:item_type>/<string:item_name>')
@API.param('item_type', f"See {NS.items._path}/types for examples")
@API.param('item_name', f"Example: 'industrial'")
class SpecificItemByType(flask_restplus.Resource):
    @limit_item_types
    @cache.cached()
    def get(self, item_type, item_name):
        """Get item by type and name"""
        data = Select('*', item_type, name=item_name).one()
        return BasicData(item_type, data=data).associative_data()


@NS.items.route('/search/<string:search_term>/')
@API.param("search_term", "Example: 'cable'")
class SearchItems(flask_restplus.Resource):
    @cache.cached()
    def get(self, search_term):
        """Search for item by name"""
        results = {}
        for table in ITEMS_TABLES:
            result = search(table, search_term)
            if "Error" not in result:
                results[table] = result
        return results


@NS.items.route('/search/<int:min_price>/<int:max_price>')
class SearchItemsByPrice(flask_restplus.Resource):
    @cache.cached()
    def get(self, min_price, max_price):
        """Search for item by price"""
        results = {}
        for table in ITEMS_TABLES:
            data = search_by_price(table, low=min_price, high=max_price)
            if "Error" not in data:
                results[table] = associative_data_dict(data, table)
        if results:
            return results
        return 204
