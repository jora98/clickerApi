from flask import Flask
from flask_cors import CORS
from common.database import db
from config.database import initialize_db
from config.resources import set_resources
from config.database import MainConfig

def create_app(config_class=MainConfig, db=db):
    app = Flask(__name__)
    CORS(app, origins="*")
    initialize_db(app, db, config_class)
    set_resources(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)