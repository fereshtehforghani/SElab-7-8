import logging
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
# from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.models.models import DrUser, PtUser
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
