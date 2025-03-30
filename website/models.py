# Where the website's database's structure will be modelled.
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Establishing the structure (fields) of the table 'Users'
class Users(db.Model, UserMixin):
    username = db.Column(db.String(16), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(150), nullable=False)
