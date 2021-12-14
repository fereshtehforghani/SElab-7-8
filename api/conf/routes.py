from flask_restful import Api

from api.services.UserServices import (
    Index,
    RegisterDr,
    RegisterPt,
    Login,
    DrProfile,
    PtProfile)


def generate_routes(app):

    # Create api.
    api = Api(app)

    # Add all routes resources.
    # Index page.
    api.add_resource(Index, "/")

    # Register page.
    api.add_resource(RegisterDr, "/auth/registerDr")
    api.add_resource(RegisterPt, "/auth/registerPt")


    # Login page.
    api.add_resource(Login, "/auth/login")

    # Profile
    api.add_resource(DrProfile, "/profileDr")
    api.add_resource(PtProfile, "/profilePt")
    #
    # # Logout page.
    # api.add_resource(Logout, "/v1/auth/logout")
    #
    # # Refresh page.
    # api.add_resource(RefreshToken, "/v1/auth/refresh")
    #
    # # Password reset page. Not forgot.
    # api.add_resource(ResetPassword, "/v1/auth/password_reset")
    #
    # # Example user handler for user permission.
    # api.add_resource(DataUserRequired, "/data_user")
    #
    # # Example admin handler for admin permission.
    # api.add_resource(DataAdminRequired, "/data_admin")
    #
    # # Example user handler for user permission.
    # api.add_resource(DataSuperAdminRequired, "/data_super_admin")
    #
    # # Get users page with admin permissions.
    # api.add_resource(UsersData, "/users")
