from flask import Flask
from flask_cors import CORS
from common.database import Database
from config.resources import set_resources

app = Flask(__name__)
CORS(app, origins="http://localhost:8100")
Database.initialize("clicker")
set_resources(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)