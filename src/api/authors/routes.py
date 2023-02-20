from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.utils.responses import response_with
import api.utils.responses as resp
from .models import Author
from .schemas import AuthorSchema

author_routes = Blueprint('author_routes', __name__)

@author_routes.route('/', methods=['GET'])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True)
    return response_with(resp.SUCCESS_200, value={'authors': author_schema.dump(fetched)})

@author_routes.route('/<int:id>', methods=['GET'])
def get_author_detail(id):
    fetched = Author.query.get(id)
    author_schema = AuthorSchema()
    return response_with(resp.SUCCESS_200, value={'author': author_schema.dump(fetched)})

@author_routes.route('/', methods=['POST'])
@jwt_required()
def create_author():
    try:
        data = request.get_json()
        if data.get('books', None) is not None:
            new_author = Author(first_name=data['first_name'], last_name=data['last_name'], books=data['books'])
        else:
            new_author = Author(first_name=data['first_name'], last_name=data['last_name'])
        new_author.create()
        author_schema = AuthorSchema()
        return response_with(resp.SUCCESS_201, value={'author': author_schema.dump(new_author)})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

@author_routes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    get_author.create()
    author_schema = AuthorSchema()
    return response_with(resp.SUCCESS_200, {'author': author_schema.dump(get_author)})

@author_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def modify_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    if data.get('first_name'):
        get_author.first_name = data['first_name']
    if data.get('last_name'):
        get_author.last_name = data['last_name']
    get_author.create()
    author_schema = AuthorSchema()
    return response_with(resp.SUCCESS_200, value={'author': author_schema.dump(get_author)})

@author_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_author(id):
    Author.query.get(id).delete()
    return response_with(resp.SUCCESS_204)
