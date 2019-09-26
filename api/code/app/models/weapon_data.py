# app/models/weapon_data.py

from slimmyorm import BaseData
from slimmyorm import Select


class WeaponData(BaseData):
    def __init__(self, name=False, table=False, data=False, category=False):
        self._table = table
        if data and category:
            data['category'] = category
        super(WeaponData, self).__init__(name, data)

    def setup(self):
        self.set_category()
        self.remove_attribute('id')

    def set_category(self):
        if not hasattr(self, 'category'):
            return
        if not isinstance(self.category, str):
            data = Select(
                'category', 'weapon_categories', where=f'id={self.category}'
                ).one()
            self.category = data['category'].title()
