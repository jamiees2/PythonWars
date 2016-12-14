import os

DEBUG = True
SECRET_KEY = ".tuW;(9Xq9V53qp'E'X*(Pa>nH+]a`@b2PuyA/xGBwCTy)](`a*"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.dirname(os.path.abspath(__file__)) + "/dev.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # TODO check if this what we really want to use
