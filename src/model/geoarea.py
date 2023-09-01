from common.database import db
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2.types import Geometry

Base = declarative_base()

#TODO find out if Base or Model is needed !!!

class GeoArea(Base, db.Model):
    __tablename__ = 'geoarea'

    id = db.Column(db.Integer, primary_key=True)
    datecreated = db.Column(db.DateTime)
    language = db.Column(db.String(20))
    last_update = db.Column(db.DateTime)
    mandant = db.Column(db.String(50))
    admincomment = db.Column(db.String)
    automaticsearch = db.Column(db.Boolean)
    name = db.Column(db.String(100))
    polygon = db.Column(Geometry(geometry_type='POLYGON'))

