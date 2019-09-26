# app/models/theme_data.py

from slimmyorm import BaseData, Select


class SpellData(BaseData):
    _table = "spells"

    def setup(self):
        self.set_spell_resistance()
        self.set_descriptors()
        self.set_school()
        self.set_range()
        self.remove_attributes(['id', 'school_id', 'range_id'])

    def set_spell_resistance(self):
        if hasattr(self, 'spell_resistance'):
            sr = self.spell_resistance
            self.spell_resistance = True if sr == 1 else False

    def set_school(self):
        if hasattr(self, 'school_id'):
            data = Select('*', 'magic_schools', db_id=self.school_id).one()
            data.pop('id')
            self.school = data

    def set_range(self):
        if hasattr(self, 'range_id'):
            data = Select('*', 'effect_ranges', db_id=self.range_id).one()
            data.pop('id')
            self.range = data

    def set_descriptors(self):
        if not hasattr(self, 'id'):
            return
        where = f"spell_id={self.id}"
        data = Select("*", "spell_descriptors", where=where).all()
        self.descriptors = []
        for item in data:
            db_id = item['descriptor_id']
            descriptor = Select("*", "descriptors", db_id=db_id).one()
            self.descriptors.append(descriptor['name'])
