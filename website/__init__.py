"""
This file causes Python to treat the 'website' directory as a package (rather than just a regular file path).
Allows for files and functions within this directory to be exported as modules to external Python files.
This file will be run as soon as this directory is imported to an external Python file.
"""
from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Loads all the variables in the '.env' file
load_dotenv()

# Defining our database object
db = SQLAlchemy()


# This is the factory function.
# Any configuration, registration, and other setup the application needs will happen inside the function.
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.getenv('DB_NAME')}"
    # Private key for the encryption of cookies
    # Loaded from the '.env' file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)

    # Imports blueprint objects from the specified file
    # This gives Flask information on how to construct the web app (structure, auth. rules, etc)
    from .views import views
    from .auth import auth

    # Tells Flask to use the above imported blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        # Usually this parameter must be 'id', hence the former inclusion of the 'id' field in the 'Users' table.
        # However, I felt that 'username' would be a more suitable primary key.
        # However, the 'flask_login' module insists that a field with the name of 'id' and, after consulting multiple...
        # ...online sources (inc. module documentation), I decided to modify the module code itself.
        # Modified file directory: /flask_login/mixin.py
        return Users.query.get(username)

    return app


def create_database(app):
    if not os.path.exists("website/" + os.getenv('DB_NAME')):
        db.create_all(app=app)
