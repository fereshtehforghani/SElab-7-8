import logging
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.models.models import DrUser, PtUser , User
# from api.roles import role_required
# from api.schemas.schemas import UserSchema


class Index(Resource):
    @staticmethod
    def get():
        return "Hello Flask Restful Example!"


class RegisterDr(Resource):
    @staticmethod
    def post():

        try:
            # Get username, password and email.
            nationalID, nezamID, password, email = (
                request.json.get("nationalID").strip(),
                request.json.get("nezamID").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("nationalID, nazamID, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if nationalID is None or nezamID is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = DrUser.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = DrUser(nationalID=nationalID, nezamID= nezamID, password=password, email=email)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {"status": "Doctor registration completed."}

class RegisterPt(Resource):
    @staticmethod
    def post():

        try:
            # Get username, password and email.
            nationalID, password, email = (
                request.json.get("nationalID").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("NationalID, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if nationalID is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = PtUser.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = PtUser(nationalID=nationalID, password=password, email=email)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {"status": "Patient registration completed."}


class Login(Resource):
    @staticmethod
    def post():

        try:
            # Get user email and password.
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if user information is none.
        if email is None or password is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email, password=password).first()

        # Check if user is not existed.
        if user is None:
            return error.UNAUTHORIZED

        if user.user_role == "user":

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(0)

        # If user is admin.
        elif user.user_role == "admin":

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(1)

        # If user is super admin.
        elif user.user_role == "sa":

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
            access_token = user.generate_auth_token(2)

        else:
            return error.INVALID_INPUT_422

        # Generate refresh token.
        refresh_token = refresh_jwt.dumps({"email": email})

        # Return access token and refresh token.
        return {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode(),
        }
