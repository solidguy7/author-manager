from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.utils.responses import response_with
import api.utils.responses as resp
from .models import Book
from .schemas import BookSchema

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('/', methods=['GET'])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True)
    return response_with(resp.SUCCESS_200, value={'books': book_schema.dump(fetched)})

@book_routes.route('/<int:id>', methods=['GET'])
def get_book_detail(id):
    fetched = Book.query.get(id)
    book_schema = BookSchema()
    return response_with(resp.SUCCESS_200, value={'book': book_schema.dump(fetched)})

@book_routes.route('/', methods=['POST'])
@jwt_required()
def create_book():
    try:
        data = request.get_json()
        new_book = Book(title=data['title'], year=data['year'], author_id=data['author_id'])
        new_book.create()
        book_schema = BookSchema()
        return response_with(resp.SUCCESS_201, value={'book': book_schema.dump(new_book)})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

@book_routes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get(id)
    get_book.title = data['title']
    get_book.year = data['year']
    get_book.create()
    book_schema = BookSchema()
    return response_with(resp.SUCCESS_200, value={'book': book_schema.dump(get_book)})

@book_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def modify_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get(id)
    if data.get('title'):
        get_book.title = data['title']
    if data.get('year'):
        get_book.year = data['year']
    get_book.create()
    book_schema = BookSchema()
    return response_with(resp.SUCCESS_200, value={'book': book_schema.dump(get_book)})

@book_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    Book.query.get(id).delete()
    return response_with(resp.SUCCESS_204)