from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.setPassword(password)

    def setPassword(self, password):
        self.password = bcrypt.encrypt(password)

    def checkPassword(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return '<User ({username})>'.format(
            username=self.username
        )
