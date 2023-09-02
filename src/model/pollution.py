from common.database import db
from config.database import Base
import uuid

class Pollution(Base):
    __tablename__ = 'pollution'

    id = db.Column(db.String(32), primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(100))
    count = db.Column(db.Integer)
    description = db.Column(db.String)
    geoarea_fk = db.Column(db.Integer, db.ForeignKey('geoarea.id'))
    
    def __init__(self, name, geoarea_fk, count=None, description=None, _id=None):
        self.name = name,
        self.count = count,
        self.description = description,
        self.geoarea_fk = geoarea_fk

    def __repr__(self) -> str:
        return f"Pollution {self.name} with count of {self.count}"