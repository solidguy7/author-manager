import unittest
from main import create_app
from .database import db
from api.config.config import TestingConfig
import tempfile

class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app(TestingConfig)
        # self.test_db_file = tempfile.mkstemp()[1]
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + self.test_db_file
        with app.app_context():
            db.create_all()
        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self) -> None:
        db.session.close_all()
        db.drop_all()
