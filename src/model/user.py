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