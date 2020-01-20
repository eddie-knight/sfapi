# app/models/class_data.py

from slimmyorm import BaseData
from slimmyorm import Select


class ClassData(BaseData):
    _table = 'classes'

    def setup(self):
        self.get_class_skills()
        self.get_level_progression()
        self.get_proficiencies()
        self.get_features()
        self.set_special_skills()
        self.set_special_children()
        self.remove_attributes(['id'])
        return self.data()

    def get_class_skills(self):
        data = Select('*', 'skills', where=f'{self.name}=1').all()
        self.skills = [
            skill['name']
            for skill in data
        ]

    def get_features(self):
        where = f"class_id={self.id}"
        data = Select('*', "class_features", where=where).all()
        self.features = {}
        for item in data:
            item.pop('class_id')
            name = item.pop('name')
            self.features[name] = item

    def set_special_skills(self):
        for f_name in self.features:
            where = (f"feature_id={self.features[f_name]['id']}"
                     " AND parent_id=0")
            data = Select('*', 'class_special_skills', where=where).all()
            if data:
                specials = {}
                for item in data:
                    name = item.pop('name')
                    specials[name] = item
                self.features[f_name]['special'] = specials
            self.features[f_name].pop('id')

    def set_special_children(self):
        f = self.features
        for name in f:
            if 'special' in f[name]:
                data = self.get_special_children(f[name]['special'])
                f[name]['special'] = data
        self.features = f

    def get_special_children(self, specials):
        for name in specials:
            where = f"parent_id={specials[name]['id']}"
            data = Select('*', 'class_special_skills', where=where).all()
            if data:
                children = {}
                for item in data:
                    item_name = item.pop('name')
                    children[item_name] = item
                specials[name]['special'] = children
            specials[name].pop('id')
        return specials

    def get_level_progression(self):
        data = Select('*', f"{self.name.lower()}_progression").all()
        self.progression = {}
        for item in data:
            name = item.pop('level')
            self.progression[f"Level {name}"] = item

    def get_proficiencies(self):
        data = Select(
            '*', 'class_proficiencies', where=f"class_id='{self.id}'"
            ).all()
        self.proficiencies = {}
        for item in data:
            feat_id = item['feat_id']
            feat = Select('*', 'feats', db_id=feat_id).one()
            self.proficiencies[feat['name']] = feat['benefit']
