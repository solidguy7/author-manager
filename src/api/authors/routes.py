import os.path
from flask import Blueprint, request, url_for, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from api.utils.responses import response_with
import api.utils.responses as resp
from .models import Author
from .schemas import AuthorSchema

allowed_extensions = {'image/jpeg', 'image/png', 'jpeg'}

def allowed_files(filename):
    return filename in allowed_extensions

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
    '''
    Create author endpoint
    ---
    parameters:
      - in: body
        name: body
        schema:
            id: Author
            required:
                - first_name
                - last_name
                - books
            properties:
                first_name:
                    type: string
                    description: First name of the author
                    default: "John"
                last_name:
                    type: string
                    description: Last name of the author
                    default: "Doe"
      - in: header
        name: authorization
        type: string
        required: true
    security:
      - Bearer: []
    responses:
        200:
            description: Author successfully created
            schema:
                id: AuthorCreated
                properties:
                    code:
                        type: string
                    message:
                        type: string
                    value:
                        schema:
                            id: AuthorFull
                            properties:
                                first_name:
                                    type: string
                                last_name:
                                    type: string
                                books:
                                    type: array
                                    items:
                                        schema:
                                            id: BookSchema
        422:
            description: Invalid input arguments
            schema:
                id: invalidInput
                properties:
                    code:
                        type: string
                    message:
                        type: string
    '''
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

@author_routes.route('/avatar/<int:author_id>', methods=['POST'])
@jwt_required()
def upsert_author_avatar(author_id):
    '''
     Upsert author avatar
    ---
    parameters:
      - in: body
        name: body
        schema:
            id: Author
            required:
                - avatar
            properties:
                avatar:
                    type: file
                    description: Image file
      - name: author_id
        in: path
        description: ID of the author
        required: true
        schema:
            type: integer
    responses:
        200:
            description: Author avatar successfully upserted
            schema:
                id: AuthorCreated
                properties:
                    code:
                        type: string
                    message:
                        type: string
                    value:
                        schema:
                            id: AuthorFull
                            properties:
                                first_name:
                                    type: string
                                last_name:
                                    type: string
                                books:
                                    type: array
                                    items:
                                        schema:
                                            id: BookSchema
        422:
            description: Invalid input arguments
            schema:
                id: invalidInput
                properties:
                    code:
                        type: string
                    message:
                        type: string
    '''
    file = request.files['avatar']
    get_author = Author.query.get(author_id)
    if file and allowed_files(file.content_type):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename))
    get_author.avatar = url_for('uploaded_file', filename=filename, _external=True)
    get_author.create()
    author_schema = AuthorSchema()
    return response_with(resp.SUCCESS_200, value={'author': author_schema.dump(get_author)})

@author_routes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    get_author.create()
    author_schema = AuthorSchema()
    return response_with(resp.SUCCESS_200, value={'author': author_schema.dump(get_author)})

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
