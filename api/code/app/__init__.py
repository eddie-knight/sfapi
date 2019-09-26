# app/__init__.py

import flask_restplus

from .constants import API

from .views import (abilities,  # noqa: F401
                    armor,  # noqa: F401
                    base_routes,  # noqa: F401
                    classes,  # noqa: F401
                    feats,  # noqa: F401
                    items,  # noqa: F401
                    races,  # noqa: F401
                    searches,  # noqa: F401
                    spells,  # noqa: F401
                    tables,  # noqa: F401
                    themes,  # noqa: F401
                    weapons)  # noqa: F401


#
# API v1
#

@API.route('/api/v1/', doc=False)
class GetAllRoutes(flask_restplus.Resource):
    def get(self):
        """List all public routes """
        rules = []
        # loop through all loops in this app
        for endpoint in API.app.url_map.iter_rules():
            rule = endpoint.rule
            # filter undocumented routes
            if ("swagger" not in rule
                    and len(rule) > 8
                    and "static" not in rule):
                # add without /api/v1 or trailing slash
                if rule[-1] == "/":
                    rule = rule[:-1]
                rules.append(rule)
        return rules if rules != [] else {"Error": "Unknown"}, 404
