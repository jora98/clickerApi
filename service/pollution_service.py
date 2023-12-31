from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from common.database import db
from model.pollution import Pollution
from model.geoarea import GeoArea

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
                'count': pollution.count,
                'description': pollution.description,
                'geoarea_fk': pollution.geoarea_fk,
                'pollution_type_fk': pollution.pollution_type_fk
            }
            json_data.append(json_item)

        return json_data
class PollutionCount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int, required=True, help="Count field is required")

    @jwt_required()
    def put(self, pollution_id: str):
        data = PollutionCount.parser.parse_args()
        pollution = Pollution.query.get(pollution_id)

        if not pollution:
            return {"message": "Pollution not found"}, 404

        pollution.count = data['count']

        try:
            db.session.commit()  # Commit the changes to the database
            return {"message": "PollutionCount updated successfully"}, 200
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return {"message": f"An error occurred while updating pollution: {str(e)}"}, 500

class PollutionDescription(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str, required=True,
                        help="Description field is required")

    @jwt_required()
    def put(self, pollution_id: str):
        data = PollutionDescription.parser.parse_args()
        pollution = Pollution.query.get(pollution_id)

        if not pollution:
            return {"message": "Pollution not found"}, 404

        pollution.description = data['description']

        try:
            db.session.commit()  # Commit the changes to the database
            return {"message": "PollutionDescription updated successfully"}, 200
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return {"message": f"An error occurred while updating pollution: {str(e)}"}, 500

class NewPollution(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pollution_type_fk', type=str, required=True,
                        help="Type field is required")
    parser.add_argument('description', type=str)
    parser.add_argument('count', type=int)
    parser.add_argument('geoarea_fk', type=int, required=True,
                        help="GeoArea foreign key is required")

    @jwt_required()
    def post(self):
        data = NewPollution.parser.parse_args()

        geoarea = db.session.query(GeoArea).get(data['geoarea_fk'])
        if not geoarea:
            return {"message": "GeoArea not found"}, 404

        pollution = Pollution(count=data['count'],
                              description=data['description'],
                              geoarea_fk=data['geoarea_fk'],
                              pollution_type_fk=data['pollution_type_fk'])

        try:
            db.session.add(pollution)
            db.session.commit()
            return {"message": "New pollution created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred while creating new pollution: {str(e)}"}, 500

class DeletePollution(Resource):

    @jwt_required()
    def delete(self, pollution_id: str):
        pollution = Pollution.query.get(pollution_id)

        if not pollution:
            return {"message": "Pollution not found"}, 404

        try:
            db.session.delete(pollution)
            db.session.commit()  # Commit the changes to the database
            return {"message": "PollutionDescription updated successfully"}, 200
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return {"message": f"An error occurred while updating pollution: {str(e)}"}, 500
