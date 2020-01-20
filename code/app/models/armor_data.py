# app/models/armor_data.py

from slimmyorm import BaseData

TYPE = {
    0: "Light Armor",
    1: "Heavy Armor",
}


class ArmorData(BaseData):
    _table = "armor"

    def setup(self):
        """Convert type_id to type listed above """
        if hasattr(self, 'type'):
            self.type = TYPE[self.type]
        self.remove_attribute('id')
