from api.utils.database import db

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', backref='Author', cascade="all, delete-orphan")
    avatar = db.Column(db.String(100), nullable=True)

    def __init__(self, first_name, last_name, books=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
