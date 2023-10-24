"""
Database Configuration Module.

Attributes:
    db (SQLAlchemy): The primary SQLAlchemy instance for the main application.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
