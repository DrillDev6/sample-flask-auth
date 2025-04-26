from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    #parametros de login id(int), username(string), password(string), email(string)

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(80), nullable=False, default='user')
    