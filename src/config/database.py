def initialize_db(_app, _db):
    _app.config['JWT_SECRET_KEY'] = '123'
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:!C0mplex@localhost/clicker'
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _db.init_app(_app)