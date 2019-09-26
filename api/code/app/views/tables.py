# app/views/tables.py

import flask_restplus

from orm import public_tables, Select
from app.constants import API, NS, cache
from app.helpers import limit_public_tables


#
# Routes
#

@NS.tables.route('/')
class GetListOfTables(flask_restplus.Resource):
    def get(self):
        """Get list of available tables for "{table}" """
        return {"tables": public_tables}


@NS.tables.route('/<string:table>/')
@API.param("table", "See /tables for examples")
class GetTableData(flask_restplus.Resource):
    @limit_public_tables
    @cache.cached()
    def get(self, table):
        """Retrieve raw data from a specified table"""
        """Get all data entries from a specified table """
        data = Select('*', table).all()
        if data == []:
            return {"Error": f"No entries found in {table}"}, 404
        if "Error" in str(data):
            return data, 500
        return data


@NS.tables.route('/<string:table>/<string:entry_name>/')
@API.param("table", "See /tables for examples")
@API.param("entry_name", "Entry to search for on provided table")
class GetTableEntry(flask_restplus.Resource):
    @limit_public_tables
    @cache.cached()
    def get(self, table, entry_name):
        """Retrieve data entry by name from a specified table"""
        data = Select('*', table, name=entry_name).one()
        if data is None:
            return {"Error": f"{entry_name} not found in {table}. "
                    f"Try this instead: {NS.search._path}/{table}/{entry_name}"
                    }, 404
        elif "Error" in str(data):
            return data, 500
        return data
