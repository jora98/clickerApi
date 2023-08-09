from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from service.geoarea_service import GeoAreas
from service.pollution_service import Pollution
from service.auth_service import Login

def set_resources(_app):
    api = Api(_app)
    jwt = JWTManager(_app)

    api.add_resource(GeoAreas, '/geoarea')
    api.add_resource(Pollution, '/pollution/byGeoarea_fk/<geoarea_fk>')
    api.add_resource(Login, '/login')
    