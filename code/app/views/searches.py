# app/views/searches.py

import flask_restplus
from slimmyorm import search_high_low

from app.constants import NS, API, cache
from app.helpers import limit_public_tables, search


#
# Helpers
#

def search_by_price(table, low=False, high=False):
    if low < 0 or high < 1:
        return {"Error": "Values must be positive numbers"}
    data = search_high_low(table, 'price', high=high, low=low)  # slimmyorm
    if data == []:
        return 204  # 204 (no content) does not support body content
    elif "Unknown column 'price'" in str(data):
        return {"Error": f"Table '{table}' does not have column 'price'"}
    return data


def table_transform(data, key):
    """Transform search data """
    table_data = {}
    for item in data:
        name = item.pop(key)
        if name in table_data:
            name = f"{name} (Level {item['level']})"
        table_data[name] = item
    return table_data


#
# Routes
#

@NS.search.route('/<string:table>/<string:search_term>/')
@API.param("table", "For examples, see /tables")
@API.param("search_term", ("Single or multi-word searches. "
                           "Order does not matter"))
class SearchTable(flask_restplus.Resource):
    @limit_public_tables
    @cache.cached()
    def get(self, table, search_term):
        """Retrieve data entry by name from a specified table"""
        data = search(table, search_term)
        return table_transform(data, 'name')


@NS.search.route('/<string:table>/<int:minimum_price>/<int:maximum_price>/')
@API.param("table", "For examples, see /tables")
@API.param("maximum_price", "Any positive whole number")
@API.param("minimum_price", "Any positive whole number (may be zero)")
@API.doc(responses={200: "success", 204: "no content found", 404: "error"})
class GetPriceList(flask_restplus.Resource):
    @limit_public_tables
    @cache.cached()
    def get(self, table, minimum_price, maximum_price):
        """Get all table entries that are under specified price"""
        data = search_by_price(table,
                               high=maximum_price,
                               low=minimum_price)
        if data == 204:
            return 204
        if "Error" in data:
            return data, 404
        return table_transform(data, 'name')
