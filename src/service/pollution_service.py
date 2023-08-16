from flask_restful import Resource, reqparse
from model.pollution import Pollution
from flask_jwt_extended import jwt_required, get_jwt_identity
from common.database import db
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

class PollutionItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int, required=True, help="Count field is required")

    @jwt_required()
    def put(self, pollution_id: str):
        data = PollutionItem.parser.parse_args()
        pollution = Pollution.query.get(pollution_id)

        if not pollution:
            return {"message": "Pollution not found"}, 404

        pollution.count = data['count']

        try:
            db.session.commit()  # Commit the changes to the database
            return {"message": "Pollution updated successfully"}, 200
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return {"message": "An error occurred while updating pollution"}, 500