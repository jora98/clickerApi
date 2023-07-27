from flask import Flask
from model.user import User
from common.database import Database

app = Flask(__name__)
Database.initialize("clicker")
User.register_user("laura@test.de", "password")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)