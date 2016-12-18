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

class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", uselist=False)
    level = db.Column(db.String)
    steps = db.Column(db.Integer)
    length = db.Column(db.Integer)
    code = db.Column(db.Text)
    score = db.Column(db.Integer)

    def __init__(self, user, level, steps, length, code, score):
        self.user_id = user.id
        self.level = level
        self.steps = steps
        self.length = length
        self.code = code
        self.score = score