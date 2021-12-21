from datetime import datetime

from flask import g
from sqlalchemy import ForeignKey

from api.conf.auth import auth, jwt
from api.database.database import db


class Prescription(db.Model):
    prescription_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer)
    patient_nat_id = db.Column(db.String(length=10))
    list_drug = db.Column(db.String(length=1000))
    comments = db.Column(db.String(length=1000))
    created = db.Column(db.DateTime, default=datetime.now)
