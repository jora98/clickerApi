"""
Database Configuration for Main and Test environments.
"""

import os
from flask import Config

class MainConfig(Config):
    """Configuration for the main environment."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:!C0mplex@clickerdb:5432/clicker'
    JWT_SECRET_KEY = '123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    """Configuration for the testing environment."""
    TESTING = True
    JWT_SECRET_KEY = '123'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:!C0mplex@db/test'
    os.environ['DATABASE_URL'] = SQLALCHEMY_DATABASE_URI

def initialize_db(_app, _db, config):
    """Initialize the database with the provided configuration."""
    _app.config.from_object(config)
    _db.init_app(_app)
