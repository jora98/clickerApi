from datetime import timedelta
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from model.user import User
from common.utils import Utils

class Login(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        user = User.query.filter_by(email=email).first()

        if user and Utils.check_hashed_password(password, user.password):
            expires = timedelta(days=7)
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            return {'token': access_token}, HTTPStatus.OK

        return {'error': 'Email or password invalid'}, HTTPStatus.UNAUTHORIZED
