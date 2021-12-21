import logging
from api.database.database import db
from api.models.userModels import User


def create_super_admin():
    user = User.query.filter_by(email="sa@gmail.com").first()
    if user is None:
        user = User(
            nationalID="0012345678",
            password="sa_password",
            email="sa@gmail.com",
            user_role="sa",
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Super admin was set.")

    else:
        logging.info("Super admin already set.")


def create_admin_user():
    user = User.query.filter_by(email="admin@gmail.com").first()
    if user is None:
        user = User(
            nationalID="1234567890",
            password="admin_password",
            email="admin@gmail.com",
            user_role="admin",
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Admin was set.")

    else:
        logging.info("Admin already set.")
