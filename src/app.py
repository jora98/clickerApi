from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from common.database import db
from config.database import initialize_db
from config.resources import set_resources

app = Flask(__name__)
CORS(app, origins="*")
initialize_db(app, db)
set_resources(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)