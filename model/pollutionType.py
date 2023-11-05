import uuid
from common.database import db

class PollutionType(db.Model):
    __tablename__ = 'pollution_type'

    id = db.Column(
        db.String(36), primary_key=True, unique=True, nullable=False,
        default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(100), nullable=False)
