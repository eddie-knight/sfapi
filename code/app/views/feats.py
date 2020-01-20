# app/views/feats.py

import flask_restplus

from app.helpers import search, data_list_to_model_dict
from app.models import FeatData
from app.constants import NS, API, cache
from orm import Select


#
# Routes
#

@NS.feats.route('/')
class GetFeats(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """All feats"""
        data = Select('*', 'feats').all()
        return data_list_to_model_dict(data, FeatData)


@NS.feats.route('/combat/')
class GetCombatFeats(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Combat feats"""
        data = Select('*', 'feats', where="combat_feat=1").all()
        return data_list_to_model_dict(data, FeatData)


@NS.feats.route('/non-combat/')
@NS.feats.route('/noncombat/', doc=False)
class GetNonCombatFeats(flask_restplus.Resource):
    @cache.cached()
    def get(self):
        """Non-combat feats"""
        data = Select('*', 'feats', where="combat_feat=0").all()
        return data_list_to_model_dict(data, FeatData)


@NS.feats.route('/<string:feat_name>/')
class GetFeatByName(flask_restplus.Resource):
    @cache.cached()
    def get(self, feat_name):
        """Specific feat, by name"""
        feat = FeatData(name=feat_name)
        if not hasattr(feat, 'benefit'):
            return {"Error": f"Feat {feat_name} not found."
                    f" Try this: {NS.feats._path}/search/"
                    f"{feat_name.replace(' ', '%20')}"
                    }, 404
        return feat.associative_data()


@NS.feats.route('/search/<string:search_term>/')
@API.param("search_term", "Example: 'master'")
class SearchFeats(flask_restplus.Resource):
    @cache.cached()
    def get(self, search_term):
        """Search for feat by name"""
        return search("feats", search_term, model=FeatData)
