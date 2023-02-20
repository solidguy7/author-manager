import logging
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from api.utils.database import db
from api.config.config import Config, TestingConfig, DevelopmentConfig
from api.utils.responses import response_with
import api.utils.responses as resp
from api.authors.routes import author_routes
from api.books.routes import book_routes
from api.users.routes import user_routes

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = Config

elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig

else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

app.register_blueprint(author_routes, url_prefix='/api/authors')
app.register_blueprint(book_routes, url_prefix='/api/books')
app.register_blueprint(user_routes, url_prefix='/api/users')

@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)

load_dotenv()

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ALGORITHM"] = "HS256"

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, use_reloader=False)
