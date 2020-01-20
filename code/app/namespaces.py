# app/namespaces.py


class Namespaces:
    def __init__(self, API):
        self.search = API.namespace(
            "Search", path="/api/v1/search")
        self.tables = API.namespace(
            "Data Tables", path="/api/v1/tables")
        self.classes = API.namespace(
            "Class Data", path="/api/v1/classes")
        self.abilities = API.namespace(
            "Ability Data", path="/api/v1/abilities")
        self.armor = API.namespace(
            "Armor Data", path="/api/v1/armor")
        self.weapon = API.namespace(
            "Weapon Data", path="/api/v1/weapons")
        self.feats = API.namespace(
            "Feat Data", path="/api/v1/feats")
        self.spells = API.namespace(
            "Spell Data", path="/api/v1/spells")
        self.items = API.namespace(
            "Item Data", path="/api/v1/items")
        self.races = API.namespace(
            "Race Data", path="/api/v1/races")
        self.themes = API.namespace(
            "Theme Data", path="/api/v1/themes")
