from common.database import Database
from common.utils import Utils
import model.errors as UserError
import uuid

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email,
        self.password = password,
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self) -> str:
        return f"User {self.email}"
    
    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512
        :param email: users e-mail (might be invalid)
        :param pasword: A sha512-hashed password
        :return: True if registered succesfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_by_email(Database.connection, "public.user", email)

        if len(user_data) != 0:
            raise UserError.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserError.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True
    
    def save_to_db(self):
        Database.insert(Database.connection, "public.user", self.json())

    def json(self):
        return {
            "id": self._id,
            "email": self.email,
            "password": self.password
        }

    