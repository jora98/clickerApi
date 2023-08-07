from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from common.database import Database
from config.resources import set_resources
from model.pollution import Pollution

app = Flask(__name__)
CORS(app, origins="http://localhost:8100")
app.config['JWT_SECRET_KEY'] = '123'
Database.initialize("clicker")
jwt = JWTManager(app)
set_resources(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)