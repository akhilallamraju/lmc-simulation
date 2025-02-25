"""
As the file name suggests, all authentication rules will be established here.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # Means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If the webpage intends to send data
    if request.method == 'POST':
        # The user-inputted data from the login/registration form in 'static/templates/login.html'
        login_or_register = request.form.get('logInOrRegister')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # User input validation for account creation/registration. The rules are:
        # - Length of username <= 16 characters
        # - Password must be at least 8 characters
        # - 'password' must be identical to 'confirm_password'
        # - Username must be unique
        if login_or_register == "register":
            if len(username) == 0 or len(password) == 0 or len(confirm_password) == 0:
                flash("One or more input fields are empty.", category="error")

            elif len(username) > 16:
                flash("Your username cannot be greater than 16 characters.", category="error")

            elif len(password) < 8:
                flash("Your password cannot be less than 8 characters.", category="error")

            elif password != confirm_password:
                flash("Your two password inputs are not the same.", category="error")

            # Username uniqueness check:
            # Queries the 'Users' table for usernames matching that of the user-inputted username.
            # '.first()' means that the 1st match will be outputted...
            # ...but, since, there cannot be more than 1 match anyway, this is completely fine
            username_matches = Users.query.filter_by(username=username).first()
            # If there is a match (ie: an account corresponding to the inputted username)
            if username_matches:
                flash("Username already exists.", category="error")

            else:
                # Account registration successful
                new_user = Users(username=username,
                                 password=generate_password_hash(password),
                                 asm_file_name="")
                db.session.add(new_user)
                db.session.commit()
                flash(message="You have successfully created an account.", category="success")
                return redirect(url_for('views.root'))

        elif login_or_register == "login":
            # Queries the 'Users' table for usernames matching that of the user-inputted username.
            # '.first()' means that the 1st match will be outputted...
            # ...but, since, there cannot be more than 1 match anyway, this is completely fine
            username_match = Users.query.filter_by(username=username).first()
            # If there is a match (ie: an account corresponding to the inputted username)
            if username_match:
                # Generates a hashed version of the user-inputted password.
                # This is then compared against the hashed password stored alongside the inputted username

                # Stupid error: 'User.password' -> 'username_match.password'.
                # Attempting to directly compare a string to an SQL table field did not work.

                # TODO: Fix error when comparing hashed passwords.
                # When hashing the password for registration and login, a different salt is being used to salt the hash.
                # Therefore, the hashed password in the database will never match the user-inputted hashed password.
                hashed_password = generate_password_hash(password)
                print(hashed_password, username_match.password)
                if check_password_hash(hashed_password, username_match.password):
                    return redirect(url_for('views.simulation'))
                else:
                    flash(message="Incorrect password.", category="error")
            else:
                flash("Username does not exist.", category="error")

    # If the webpage intends to receive data
    elif request.method == 'GET':
        pass

    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<h1>Logout Page</h1>"


@auth.route('/simulation')
def simulation():
    return render_template("simulation.html")
