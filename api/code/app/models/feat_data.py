# app/models/feat_data.py

from slimmyorm import BaseData
from slimmyorm import Select


class FeatData(BaseData):
    _table = "feats"

    def setup(self):
        self.combat_feat = True if self.combat_feat else False
        if not self.extra_text:
            self.remove_attribute('extra_text')
        self.set_modifier()
        self.remove_attributes(['id', 'modifier_id'])

    def set_modifier(self):
        if self.modifier_id:
            where = f"id={self.modifier_id}"
            data = Select("*", "modifiers", where=where).one()
            self.modifier = data['name']
