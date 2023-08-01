from sre_parse import TYPE_FLAGS
from flask_restful import Resource
from common.database import Database


class Pollution(Resource):
    def get(self):
        pollution =  Database.find_all(Database.connection, "public.pollution")
        return Pollution.json(pollution)
    
    @staticmethod   
    def json(_pollution):
        json_data = []
        for item in _pollution:
            json_item = {
                'id': item[0],
                'Zigarettenstummel': item[1],
                'Essensreste': [2],
                'Drogenabfälle': [3],
                'Tierische Verschmutzung': item[4],
                'Pflanzliche Verschmutzung': item[5],
                'geoarea_fk': item[6]
            }
            json_data.append(json_item)

        return json_data