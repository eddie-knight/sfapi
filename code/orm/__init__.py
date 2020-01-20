# orm/__init__.py

from pathlib import Path
from slimmyorm import SlimMyJson, Select  # noqa: F401

public_tables = [
            str(path).replace(".json", "").replace("/code/orm/json/", "")
            for path in Path.cwd().rglob("json/*.json")
        ]


def setup():
    """
    For debugging, add this route:
        @API.route('/setup')
        class TestSetup(flask_restplus.Resource):
            def get(self):
                return setup()
    """
    return SlimMyJson().results  # For debugging
