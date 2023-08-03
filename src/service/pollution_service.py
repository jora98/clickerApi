from sre_parse import TYPE_FLAGS
from flask_restful import Resource
from common.database import Database

#TO DO !!! change service to the correct model

class Pollution(Resource):

    @staticmethod
    def get(geoarea_fk: int):
        print("geoarea_fk" + str(geoarea_fk))
        pollution =  Database.find_by_id(Database.connection, "public.pollution", f"geoarea_fk = {geoarea_fk}")
        print(pollution)
        
        return Pollution.json(pollution)
    

    
    @staticmethod   
    def json(_pollution):
        json_data = []
        for item in _pollution:
            json_item = {
                'id': item[0],
                'name': item[1],
                'count': [2],
                'description': [3],
                'geoarea_fk': item[4]
            }
            json_data.append(json_item)

        return json_data