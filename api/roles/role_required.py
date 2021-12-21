import functools
import logging
from flask import request
import api.error.errors as error
from api.conf.auth import jwt


def permission(arg):
    def check_permissions(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if auth is None and "Authorization" in request.headers:
                try:
                    auth_type, token = request.headers["Authorization"].split(None, 1)
                    data = jwt.loads(token)
                    if data["admin"] < arg:
                        return error.NOT_ADMIN
                except ValueError:
                    return error.HEADER_NOT_FOUND
                except Exception as why:
                    logging.error(why)
                    return error.INVALID_INPUT_422
            return f(*args, **kwargs)
        return decorated
    return check_permissions


def permission_prescription(arg):
    def check_permissions_doctor(f):
        @functools.wraps(f)
        def decorated_presc(*args, **kwargs):
            auth = request.authorization
            if auth is None and "Authorization" in request.headers:
                try:
                    auth_type, token = request.headers["Authorization"].split(None, 1)
                    data = jwt.loads(token)
                    if data["user"] > arg:
                        return error.NOT_Doctor
                except ValueError:
                    return error.HEADER_NOT_FOUND
                except Exception as why:
                    logging.error(why)
                    return error.INVALID_INPUT_422
            return f(*args, **kwargs)
        return decorated_presc
    return check_permissions_doctor
