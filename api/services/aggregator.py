import logging
import requests
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth
from api.services.PrescServices import PrescriptionList


class PatientPrescriptions(Resource):
    @staticmethod
    @auth.login_required
    def get():
        try:
            presc = PrescriptionList.get()
            presc_json = {}
            for p in presc:
                doctor_id = p.doctor_id
                dr_info = requests.post('http://localhost:5000/DrInfo', json={"dr_id": doctor_id})
                presc_json["%s" % p.prescription_id] = {'drugs': '%s' % p.list_drug, 'comments': '%s' % p.comments,
                                                        'Doctor': '%s' % dr_info.json()}
            return presc_json
        except Exception as why:
            logging.error(why)
            return error.INVALID_INPUT_422
