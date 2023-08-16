from flask_jwt_extended import JWTManager
from flask_restful import Api
from service.geoarea_service import GeoAreas
from service.pollution_service import Pollutions, PollutionItem
from service.auth_service import Login
from service.auth_service import Register

def set_resources(_app):
    api = Api(_app)
    jwt = JWTManager(_app)

    api.add_resource(GeoAreas, '/geoarea')
    api.add_resource(Pollutions, '/pollution/byGeoarea_fk/<geoarea_fk>')
    api.add_resource(PollutionItem, '/pollution/pollutionUpdate/<pollution_id>')
    api.add_resource(Login, '/login')
    api.add_resource(Register, '/register')