import logging
# import jsonify

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth
from api.database.database import db
from api.models.userModels import DrUser, PtUser, User
from api.roles import role_required


class Index(Resource):
    @staticmethod
    def get():
        return "Doctor Patient Restful API!"


class RegisterDr(Resource):
    @staticmethod
    def post():

        try:
            nationalID, name, nezamID, password, email = (
                request.json.get("nationalID").strip(),
                request.json.get("name").strip(),
                request.json.get("nezamID").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:
            logging.info("nationalID, nazamID, password or email is wrong. " + str(why))
            return error.INVALID_INPUT_422

        if nationalID is None or nezamID is None or password is None or email is None:
            return error.INVALID_INPUT_422
        user = DrUser.query.filter_by(email=email).first()
        if user is not None:
            return error.ALREADY_EXIST
        user = DrUser(nationalID=nationalID, name=name, nezamID=nezamID, password=password, email=email,
                      user_role="doctor")
        db.session.add(user)
        db.session.commit()
        return {"status": "Doctor registration completed."}


class RegisterPt(Resource):
    @staticmethod
    def post():

        try:
            nationalID, name, password, email = (
                request.json.get("nationalID").strip(),
                request.json.get("name").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:
            logging.info("NationalID, password or email is wrong. " + str(why))
            return error.INVALID_INPUT_422
        if nationalID is None or password is None or email is None:
            return error.INVALID_INPUT_422

        user = PtUser.query.filter_by(email=email).first()
        if user is not None:
            return error.ALREADY_EXIST
        user = PtUser(nationalID=nationalID, name=name, password=password, email=email, user_role="patient")
        db.session.add(user)
        db.session.commit()
        return {"status": "Patient registration completed."}


class Login(Resource):
    @staticmethod
    def post():
        try:
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )
        except Exception as why:
            logging.info("Email or password is wrong. " + str(why))
            return error.INVALID_INPUT_422
        if email is None or password is None:
            return error.INVALID_INPUT_422
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            return error.UNAUTHORIZED
        if user.user_role == "doctor":
            access_token = user.generate_auth_token(0, doc_or_pat="doctor")
        elif user.user_role == "patient":
            access_token = user.generate_auth_token(0, doc_or_pat="patient")
        elif user.user_role == "admin":
            access_token = user.generate_auth_token(1)
        elif user.user_role == "sa":
            access_token = user.generate_auth_token(2)
        else:
            return error.INVALID_INPUT_422
        return {"access_token": access_token.decode()}


class AdminProfile(Resource):
    @auth.login_required
    def get(self):
        user = (User.query.filter_by(email=g.user).first())
        print(user.nationalID)
        return {'role': 'Admin', 'NationalID': '%s' % user.nationalID, 'Name': '%s' % user.name,
                'Email': '%s' % user.email}


class DrProfile(Resource):
    @auth.login_required
    def get(self):
        user = (DrUser.query.filter_by(email=g.user).first())
        print(user.nationalID)
        return {'role': 'Doctor'
                        '', 'NationalID': '%s' % user.nationalID, 'Name': '%s' % user.name, 'Email': '%s' % user.email, 'NezamID': '%s' % user.nezamID}


class PtProfile(Resource):
    @auth.login_required
    def get(self):
        user = (PtUser.query.filter_by(email=g.user).first())
        print(user.nationalID)
        return {'role': 'Patient', 'NationalID': '%s' % user.nationalID, 'Name': '%s' % user.name,
                'Email': '%s' % user.email}


class DrList(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        try:
            user_json = {}
            users = DrUser.query.all()
            for user in users:
                user_json["%s" % user.id] = {'NationalID': '%s' % user.nationalID, 'Name': '%s' % user.name,
                                             'Email': '%s' % user.email, 'nezamID': '%s' % user.nezamID}
            print(user_json)
            return user_json
        except Exception as why:
            logging.error(why)
            return error.INVALID_INPUT_422


class PtList(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        try:
            user_json = {}
            users = PtUser.query.all()
            for user in users:
                user_json["%s" % user.id] = {'NationalID': '%s' % user.nationalID, 'Name': '%s' % user.name,
                                             'Email': '%s' % user.email}
            print(user_json)
            return user_json

        except Exception as why:
            logging.error(why)
            return error.INVALID_INPUT_422


class DrInfo(Resource):
    @staticmethod
    def post():
        dr_id = request.json.get("dr_id")
        user = DrUser.query.filter_by(dr_id=dr_id).first()
        print(user)
        return {'role': 'Doctor', 'Name': '%s' % user.name, 'NezamID': '%s' % user.nezamID}
