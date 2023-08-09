from flask_restful import Resource
from model.geoarea import GeoArea

class GeoAreas(Resource):
    def get(self):
        geoareas = GeoArea.query.all()
        return GeoAreas.json(geoareas)
        
    @staticmethod   
    def json(_geoareas):
        json_data = []
        for geoarea in _geoareas:
            json_item = {
                'id': geoarea.id,
                'datecreated': geoarea.datecreated.isoformat() if geoarea.datecreated else None,
                'language': geoarea.language,
                'last_update': geoarea.last_update.isoformat() if geoarea.last_update else None,
                'mandant': geoarea.mandant,
                'admincomment': geoarea.admincomment,
                'automaticsearch': geoarea.automaticsearch,
                'name': geoarea.name,
                'polygon': geoarea.polygon
            }
            json_data.append(json_item)

        return json_data
