import datetime
from http import HTTPStatus
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from common.database import Database
from common.utils import Utils

class Login(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        email = args['email']
        password = args['password']
        #have to change the datatype of data to properly use it. change password and id with variable !!!
        data = Database.find_by_email(Database.connection, "public.user", email)
        print(password, data)
        if data and Utils.check_hashed_password(password, '$pbkdf2-sha512$25000$lbIWIuTcW8u5N.b8f0.p1Q$5GXnYgjshqKW8rR3f9Us3.BkmkTIgOKOsMTVWQCKWXhe7giV8apahJkLxQ/UHOhRMhEI5pyEawjOHkKE/DF/tQ'):
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str('818fca6af1a2496e9818b742ede2c00d'), expires_delta=expires)
            return {'token': access_token}, HTTPStatus.OK

        return {'error': 'Email or password invalid'}, HTTPStatus.UNAUTHORIZED
