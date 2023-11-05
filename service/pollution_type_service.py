from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from common.database import db
from model.pollutionType import PollutionType

class PollutionTypes(Resource):
    def get(self):
        pollution_type = PollutionType.query.all()
        return PollutionTypes.json(pollution_type)
    
    @staticmethod
    def json(_pollution_type):
        json_data = []
        for pollution_type in _pollution_type:
            json_item = {
                'id': pollution_type.id,
                'name': pollution_type.name
            }
            json_data.append(json_item)

        return json_data
    
class NewPollutionType(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)

    @jwt_required()
    def post(self):
        data = NewPollutionType.parser.parse_args()

        pollutionType = PollutionType(name=data['name'])

        try:
            db.session.add(pollutionType)
            db.session.commit()
            return {"message": "New pollution type created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred while creating new pollution type: {str(e)}"}, 500