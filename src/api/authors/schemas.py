from api.utils.database import db
from .models import Author
from api.books.schemas import BookSchema
from marshmallow import Schema, fields

class AuthorSchema(Schema):
    class Meta(Schema.Meta):
        model = Author
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.String(dump_only=True)
    books = fields.Nested(BookSchema, many=True)
