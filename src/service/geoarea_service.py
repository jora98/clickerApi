from sre_parse import TYPE_FLAGS
from flask_restful import Resource
from common.database import Database
import json
from datetime  import datetime, time


class GeoAreas(Resource):
    def get(self):
        geoareas =  Database.find_all(Database.connection, "public.geoarea")
        return GeoAreas.json(geoareas)
        
        
    @staticmethod   
    def json(_geoareas):
        json_data = []
        for item in _geoareas:
            json_item = {
                'id': item[0],
                'datecreated': item[1].isoformat() if isinstance(item[1], time) else None,
                'language': item[2],
                'last_update': item[3].isoformat() if isinstance(item[3], datetime) else None,
                'mandant': item[4],
                'admincomment': item[5],
                'automaticsearch': item[6],
                'name': item[7],
                'polygon': item[8]
            }
            json_data.append(json_item)

        json_string = json.dumps(json_data, indent=2)
        print( type(json_data))
        return json_data

