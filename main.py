import os
from flask import Flask
from api.conf.config import SQLALCHEMY_DATABASE_URI
from api.conf.routes import generate_routes
from api.database.database import db
from api.database.db_initializer import (create_admin_user,
                                               create_super_admin,
                                               create_test_user)


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    generate_routes(app)
    db.init_app(app)
    if not os.path.exists(SQLALCHEMY_DATABASE_URI):
        db.app = app
        db.create_all()
        create_super_admin()
        create_admin_user()
        create_test_user()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)
