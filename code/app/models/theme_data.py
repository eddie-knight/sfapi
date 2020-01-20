# app/models/theme_data.py

from slimmyorm import BaseData, Select


class ThemeData(BaseData):
    _table = "themes"

    def setup(self):
        self.add_theme_modifiers()
        self.remove_attribute('id')

    def add_theme_modifiers(self):
        theme_mods = Select('*',
                            'theme_modifiers',
                            where=f'theme_id={self.id}').all()
        mod_ids = [
            mod['modifier_id']
            for mod in theme_mods
        ]
        mods = []
        for mod_id in mod_ids:
            data = Select('name', 'modifiers', where=f'id={mod_id}').one()
            mods.append(data['name'])
        self.creation_modifiers = mods
