from common.database import Database
from common.utils import Utils
import model.errors as UserError
import uuid

class Pollution(object):
    def __init__(self, name, geoarea_fk, count=None, description=None, _id=None):
        self.name = name,
        self.count = count,
        self.description = description,
        self.geoarea_fk = geoarea_fk,
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self) -> str:
        return f"Pollution {self.name} with count of {self.count}"
    
    @staticmethod
    def create_pollution(name, count, description, geoarea_fk):
        """
        TO DO !!!
        """
        pollution_data = Database.find(Database.connection, "public.pollution", "where name = %s and geoarea_fk = %s", (name, geoarea_fk))
        
        if len(pollution_data) != 0:
            raise UserError.UserAlreadyRegisteredError("The pollution you tried to creat already exists for this area.")

        Pollution(name,geoarea_fk, count, description).save_to_db()

        return True
    
    def save_to_db(self):
        Database.insert(Database.connection, "public.pollution", self.json())

    def json(self):
        return {
            "id": self._id,
            "name": self.name,
            "count": self.count,
            "description": self.description,
            "geoarea_fk": self.geoarea_fk
        }

    