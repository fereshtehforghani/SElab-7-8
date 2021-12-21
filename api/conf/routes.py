from flask_restful import Api

from api.services.PrescServices import CreatePrescription
from api.services.UserServices import (
    Index,
    RegisterDr,
    RegisterPt,
    Login,
    DrProfile,
    PtProfile,
    DrList,
    PtList,
    AdminProfile, DrInfo)
from api.services.aggregator import PatientPrescriptions


def generate_routes(app):

    # Create api
    api = Api(app)

    # Index page
    api.add_resource(Index, "/")

    # Register page
    api.add_resource(RegisterDr, "/auth/registerDr")
    api.add_resource(RegisterPt, "/auth/registerPt")

    # Login page
    api.add_resource(Login, "/auth/login")

    # Profile
    api.add_resource(AdminProfile, "/profileAdmin")
    api.add_resource(DrProfile, "/profileDr")
    api.add_resource(PtProfile, "/profilePt")

    # lists
    api.add_resource(DrList, "/admin/listDr")
    api.add_resource(PtList, "/admin/listPt")

    # prescription
    api.add_resource(CreatePrescription, "/create_prescription")
    api.add_resource(PatientPrescriptions, "/patient_prescription_list")
    api.add_resource(DrInfo, "/DrInfo")
