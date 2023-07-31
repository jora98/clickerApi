from flask_restful import Api, Resource
from service.geoarea_service import GeoAreas



def set_resources(_app):
    api = Api(_app)

    api.add_resource(GeoAreas, '/geoarea')