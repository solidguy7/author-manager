from flask import Blueprint, request, url_for, render_template_string
from flask_jwt_extended import create_access_token
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email
from .models import User
from .schemas import UserSchema

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        return response_with(resp.SERVER_ERROR_404)
    user = User.find_by_email(email)
    if user.isVerified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.isVerified = True
        user.create()
        return response_with(resp.SUCCESS_200, value={'message': 'E-mail verified, you can proceed to login now.'})

@user_routes.route('/', methods=['POST'])
def create_user():
    try:
        password = User.generate_hash(request.json['password'])
        email = request.json['email']
        new_user = User(username=request.json['username'], password=password, email=email)
        new_user.create()
        token = generate_verification_token(email)
        verification_email = url_for('user_routes.verify_email', token=token, _external=True)
        html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link to activate your "
                                      "account:</p> <p><a href='{{ verification_email }}'>"
                                      "{{ verification_email }}</a></p> <br> <p>Thanks!</p>",
                                      verification_email=verification_email)
        subject = 'Please Verify your email'
        send_email(new_user.email, subject, html)
        user_schema = UserSchema()
        return response_with(resp.SUCCESS_201, value={'user': user_schema.dump(new_user)})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        if data.get('email'):
            auth = data['email']
            user = User.find_by_email(auth)
        elif data.get('username'):
            auth = data['username']
            user = User.find_by_username(auth)
        if not user:
            return response_with(resp.SERVER_ERROR_404)
        if user and not user.isVerified:
            return response_with(resp.BAD_REQUEST_400)
        if User.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity=auth)
            return response_with(resp.SUCCESS_201, value={'message': f'Logged in as {user.username}',
                                                          'access_token': access_token})
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception:
        return response_with(resp.INVALID_INPUT_422)
