# app/views/base_routes.py

from app.constants import APP, NS
from flask import jsonify


#
# Helpers
#

def get_attributes(object):
    """Returns all public attributes of an object """
    return [attribute for attribute, value in vars(object).items() if
            not (attribute.startswith('_') or callable(attribute))]


def routes():
    """Returns base routes for all namespaces """
    paths = []
    for namespace in get_attributes(NS):
        attr = getattr(NS, namespace)
        paths.append(attr._path)
    return paths


def list_routes(namespace):
    """Get all routes for given namespace """
    items = []
    for item in namespace.resources:
        path = str(item[1][0])  # get individual path
        items.append(f"{namespace._path}{path}")  # add base route to path
    items.sort()  # sort routes alphabetically
    return items


#
# Routes
#

@APP.route("/<path:route>")
def list_child_routes(route):
    """Route for all namespace base paths """
    # Add / to the beginning of the route
    if f"/{route}" not in routes():
        # If route isn't a base route, return error
        return {"Error": "(404) Route Not Found"}, 404

    # If the last character in the route is /, strip it
    route = route[:-1] if route[-1] == "/" else route

    # get namespace that matches this route
    namespace = getattr(NS, route[7:])

    # get a list of routes for namespace, and convert to json
    return jsonify(list_routes(namespace))
