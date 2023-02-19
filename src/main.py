import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.config.config import Config, TestingConfig, DevelopmentConfig

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = Config

elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig

else:
    app_config = DevelopmentConfig

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    create_app(app_config).run(host='0.0.0.0', port=8000, use_reloader=False)
