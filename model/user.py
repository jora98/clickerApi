"""
This module defines the User model."""

import uuid
from common.utils import Utils
from common.database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(
        db.String(32), primary_key=True, unique=True, nullable=False,
        default=lambda: uuid.uuid4().hex)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = Utils.hash_password(password)
