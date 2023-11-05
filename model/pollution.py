"""
This module defines the Pollution model,
representing pollution data associated with specific geoareas.
"""

import uuid
from common.database import db

class Pollution(db.Model):
    __tablename__ = 'pollution'

    id = db.Column(
        db.String(32), primary_key=True, unique=True, nullable=False,
        default=lambda: uuid.uuid4().hex)
    count = db.Column(db.Integer)
    description = db.Column(db.String)
    geoarea_fk = db.Column(db.Integer, db.ForeignKey('geoarea.id'))
    pollution_type_fk = db.Column(db.String, db.ForeignKey('pollution_type.id'))

    def __init__(self, geoarea_fk, pollution_type_fk, count=None, description=None, _id=None):
        self.count = count
        self.description = description
        self.geoarea_fk = geoarea_fk
        self.pollution_type_fk = pollution_type_fk
