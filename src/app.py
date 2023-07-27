from flask import Flask
from common.database import Database

app = Flask(__name__)
Database.initialize("clicker")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)