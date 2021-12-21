from datetime import datetime
from flask import g
from sqlalchemy import ForeignKey
from api.conf.auth import auth, jwt
from api.database.database import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    nationalID = db.Column(db.String(length=10))
    name = db.Column(db.String(length=10))
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.now)
    user_role = db.Column(db.String, default="user")

    def generate_auth_token(self, permission_level, doc_or_pat="admin"):
        if doc_or_pat == "admin":
            if permission_level == 1:
                token = jwt.dumps({"email": self.email, "admin": 1})
                return token
            elif permission_level == 2:
                token = jwt.dumps({"email": self.email, "admin": 2})
                return token
        else:
            if doc_or_pat == "doctor":
                token = jwt.dumps({"email": self.email, "admin": 0, "user": 0})
                return token
            else:
                token = jwt.dumps({"email": self.email, "admin": 0, "user": 1})
                return token

    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        g.user = None
        try:
            data = jwt.loads(token)
        except:
            return False
        if "email" and "admin" in data:
            g.user = data["email"]
            g.admin = data["admin"]
            return True
        return False

    def __repr__(self):
        return "<User(id='%s', nationalID='%s', name='%s', password='%s', email='%s', created='%s')>" % (
            self.id,
            self.nationalID,
            self.name,
            self.password,
            self.email,
            self.created,
        )


class DrUser(User):
    __tablename__ = 'DrUser'
    dr_id = db.Column(db.Integer, ForeignKey('User.id'), primary_key=True)
    nezamID = db.Column(db.String(length=80), unique=True)

    def __repr__(self):
        return "<User(id='%s', nationalID='%s', name='%s', nezamID='%s', email='%s', created='%s')>" % (
            self.id,
            self.nationalID,
            self.name,
            self.nezamID,
            self.email,
            self.created,
        )


class PtUser(User):
    __tablename__ = 'PtUser'
    Pt_id = db.Column(db.Integer, ForeignKey('User.id'), primary_key=True)
