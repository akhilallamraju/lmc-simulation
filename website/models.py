# Where the website's database's structure will be modelled.
from . import db
from flask_login import UserMixin


# Establishing the structure (fields) of the table 'Users'
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    asm_file_name = db.Column(db.String(150), nullable=False)
