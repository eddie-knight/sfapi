# app/helpers.py

from orm import public_tables, Select
from app.constants import APP


def get_as_object(table, model, where=False, category=False):
    """Get entry as data objects """
    items = Select('*', table, where=where).all()
    if not items:
        return {"Error": "No entries found fitting this description"}

    data = {}
    for item in items:
        name = item.pop('name')
        if category:
            weapon = model(data=item, category=category)
        else:
            weapon = model(data=item)
        data[name] = weapon.data()
    return data


def limit_public_tables(function):
    def limit(*args, **kwargs):
        if 'table' in kwargs:
            if kwargs['table'] not in public_tables:
                return f"Error: Table '{kwargs['table']}' does not exist.", 404
        return function(*args, **kwargs)
    return limit


def data_list_to_model_dict(data_list, model):
    if "Error" in data_list:
        APP.logger.info(data_list)
    APP.logger.info(f"Results in query: {len(data_list)}")
    result_list = {}
    for item in data_list:
        result = model(data=item).data()
        name = result.pop('name')
        result_list[name] = result
    return result_list


def search(table, name, where=False, model=False):
    data = Select('*', table, search=True, name=name, where=where).all()
    if data == []:
        return {"Error": f"'{name}' not found when searching"}
    if "Error" in str(data):
        return data, 500
    if model:
        return data_list_to_model_dict(data, model)
    return data
