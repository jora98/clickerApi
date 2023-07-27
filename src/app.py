from flask import Flask
from common.database import initialize

app = Flask(__name__)
initialize()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)