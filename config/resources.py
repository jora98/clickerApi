"""
Resource setup for the API endpoints. Associates endpoints with their respective services.
"""

from flask_jwt_extended import JWTManager
from flask_restful import Api
from service.geoarea_service import GeoAreas
from service.pollution_service import (
    Pollutions, PollutionCount, PollutionDescription, NewPollution, DeletePollution
)
from service.pollution_type_service import NewPollutionType, PollutionTypes
from service.auth_service import Login
from service.auth_service import Register

def set_resources(_app):
    """
    Initializes API resources and adds them to the application.
    """
    api = Api(_app)
    JWTManager(_app)

    api.add_resource(GeoAreas, '/geoarea')
    api.add_resource(Pollutions, '/pollution/byGeoarea_fk/<geoarea_fk>')
    api.add_resource(PollutionTypes, '/pollutionTypes')
    api.add_resource(NewPollutionType, '/pollutionTypes/newPollutionType')
    api.add_resource(PollutionCount, '/pollution/pollutionCount/<pollution_id>')
    api.add_resource(PollutionDescription, '/pollution/pollutionDescription/<pollution_id>')
    api.add_resource(NewPollution, '/pollution/newPollution')
    api.add_resource(DeletePollution, '/pollution/deletePollution/<pollution_id>')
    api.add_resource(Login, '/login')
    api.add_resource(Register, '/register')
