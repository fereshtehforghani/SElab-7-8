from marshmallow import Schema, fields


class BaseUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    nationalID = fields.Str()
    email = fields.Str()
    # password = fields.Str()
    created = fields.Str()


class UserSchema(Schema):
    nationalID = fields.Str()
    name = fields.Str()
    email = fields.Str()
    created = fields.Str()


class DrUserSchema(UserSchema):
    nezamID = fields.Str()


class PtUserSchema(UserSchema):
    pass
