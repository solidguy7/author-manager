from marshmallow import Schema, fields
from api.utils.database import db
from .models import User

class UserSchema(Schema):
    class Meta(Schema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
