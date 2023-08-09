from flask_restful import Resource
from model.pollution import Pollution

class Pollutions(Resource):
    def get(self, geoarea_fk: int):
        pollution = Pollution.query.filter_by(geoarea_fk=geoarea_fk).all()
        return Pollutions.json(pollution)
    
    @staticmethod   
    def json(_pollution):
        json_data = []
        for pollution in _pollution:
            json_item = {
                'id': pollution.id,
                'name': pollution.name,
                'count': pollution.count,
                'description': pollution.description,
                'geoarea_fk': pollution.geoarea_fk
            }
            json_data.append(json_item)

        return json_data
