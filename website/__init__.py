"""
This file causes Python to treat the 'website' directory as a package (rather than just a regular file path).
Allows for files and functions within this directory to be exported as modules to external Python files.
This file will be run as soon as this directory is imported to an external Python file.
"""
from flask import Flask
from dotenv import load_dotenv
import os

# Loads all the variables in the '.env' file
load_dotenv()


# This is the factory function.
# Any configuration, registration, and other setup the application needs will happen inside the function.
def create_app():
    app = Flask(__name__)
    # Private key for the encryption of cookies
    # Loaded from the '.env' file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Imports blueprint objects from the specified file
    # This gives Flask information on how to construct the web app (structure, auth. rules, etc)
    from .views import views
    from .auth import auth

    # Tells Flask to use the above imported blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
