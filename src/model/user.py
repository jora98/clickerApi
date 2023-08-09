from flask_sqlalchemy import SQLAlchemy
from common.utils import Utils
import model.errors as UserError
from common.database import db
import uuid

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = Utils.hash_password(password)

    def __repr__(self) -> str:
        return f"User {self.email}"

    @staticmethod
    def register_user(email, password):
        # Check if the user already exists and validate the email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise UserError.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserError.InvalidEmailError("The e-mail does not have the right format.")

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return new_user