from api.utils.database import db
from .models import Book
from marshmallow import Schema, fields

class BookSchema(Schema):
    class Meta(Schema.Meta):
        model = Book
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    year = fields.Integer(required=True)
    author_id = fields.Integer()
