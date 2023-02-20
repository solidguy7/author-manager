from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from api.utils.responses import response_with
from api.utils import responses as resp
from .models import User
from .schemas import UserSchema

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['POST'])
def create_user():
    try:
        username = request.json['username']
        password = User.generate_hash(request.json['password'])
        new_user = User(username=username, password=password)
        new_user.create()
        user_schema = UserSchema()
        return response_with(resp.SUCCESS_201, value={'user': user_schema.dump(new_user)})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return response_with(resp.SUCCESS_201, value={'message': f'Logged in as {current_user.username}',
                                                          'access_token': access_token})
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception:
        return response_with(resp.INVALID_INPUT_422)
