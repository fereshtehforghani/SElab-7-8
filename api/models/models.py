from datetime import datetime

from flask import g

from api.conf.auth import auth, jwt
from api.database.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nationalID = db.Column(db.String(length=10))
    name = db.Column(db.String(length=10))
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_role = db.Column(db.String, default="user")

    def generate_auth_token(self, permission_level):
        if permission_level == 1:
            token = jwt.dumps({"email": self.email, "admin": 1})
            return token

        elif permission_level == 2:
            token = jwt.dumps({"email": self.email, "admin": 2})
            return token

        return jwt.dumps({"email": self.email, "admin": 0})

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
    nezamID = db.Column(db.String(length=80))

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
    pass
