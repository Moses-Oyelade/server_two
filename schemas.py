from marshmallow import fields, Schema


class UserSchema(Schema):
    userId = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String()
 