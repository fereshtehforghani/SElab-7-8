import logging
from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth
from api.database.database import db
from api.models.prescriptionModel import Prescription
from api.models.userModels import DrUser, PtUser, User
from api.roles import role_required


class CreatePrescription(Resource):
    @staticmethod
    @auth.login_required
    @role_required.permission_prescription(0)
    def post():
        try:
            patient_nat_id, list_drug, comments = (
                request.json.get("patient_nat_id").strip(),
                request.json.get("list_drug").strip(),
                request.json.get("comments").strip()
            )
        except Exception as why:
            logging.info("patient_nat_id, doc_id, list_drugs or comment is wrong. " + str(why))
            return error.INVALID_INPUT_422

        if PtUser.query.filter_by(nationalID=patient_nat_id).first() is None:
            return error.DOES_NOT_EXIST
        dr_user = DrUser.query.filter_by(email=g.user).first()
        prescription = Prescription(patient_nat_id=patient_nat_id, doctor_id=dr_user.dr_id, list_drug=list_drug,
                                    comments=comments)
        db.session.add(prescription)
        db.session.commit()
        return {"status": "Create prescription completed."}


class PrescriptionList(Resource):
    @staticmethod
    @auth.login_required
    def get():
        try:
            user = (PtUser.query.filter_by(email=g.user).first())
            presc = Prescription.query.filter_by(patient_nat_id=user.nationalID).all()
            return presc
        except Exception as why:
            logging.error(why)
            return error.INVALID_INPUT_422
