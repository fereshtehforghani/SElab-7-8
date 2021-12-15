import logging

from api.database.database import db
from api.models.models import User, PtUser


def create_super_admin():
    user = User.query.filter_by(email="sa_email@example.com").first()
    if user is None:
        user = User(
            nationalID="sa_username",
            password="sa_password",
            email="sa_email@example.com",
            user_role="sa",
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Super admin was set.")

    else:
        logging.info("Super admin already set.")


def create_admin_user():
    user = User.query.filter_by(email="admin_email@example.com").first()
    if user is None:
        user = User(
            nationalID="admin_username",
            password="admin_password",
            email="admin_email@example.com",
            user_role="admin",
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Admin was set.")

    else:
        logging.info("Admin already set.")


def create_test_patient_user(
    nationalID="test_username",
    name="test_name",
    password="test_password",
    email="test_email@example.com",
    user_role="user",
):

    user = PtUser.query.filter_by(email="test_email@example.com").first()

    if user is None:
        # user = User(username=username, password=password, email=email, user_role=user_role)
        user = PtUser(
            nationalID=nationalID,
            name=name,
            password=password,
            email=email,
            user_role=user_role,
        )

        db.session.add(user)
        db.session.commit()
        logging.info("Test user was set.")
        return user

    else:
        logging.info("User already set.")


