from flask import Config
import os

class MainConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:!C0mplex@localhost/clicker'
    JWT_SECRET_KEY = '123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    JWT_SECRET_KEY = '123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

def initialize_db(_app, _db, config):
    _app.config.from_object(config)
    _db.init_app(_app)



