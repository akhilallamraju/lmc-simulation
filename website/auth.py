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
            # PATCHED ERROR: If 'password' was < 8 characters but was the same as 'confirm_password', the account...
            # ...would still be made.
            # FIX: 'valid' Boolean added. If any of the validation rules are violated, the Boolean would be set to...
            # ...False. This Boolean is now the condition for instantiating an account in the database so, a...
            # ...new account can now only be made if none of the if statements prior are triggered.
            # REPRODUCE ERROR: Remove all references to 'valid' below and change, from the 2nd if statement, all if...
            # ...statements to 'elif'.
            valid = True
            if len(username) == 0 or len(password) == 0 or len(confirm_password) == 0:
                valid = False
                flash("One or more input fields are empty.", category="error")

            if len(username) > 16:
                valid = False
                flash("Your username cannot be greater than 16 characters.", category="error")

            if len(password) < 8:
                valid = False
                flash("Your password cannot be less than 8 characters.", category="error")

            if password != confirm_password:
                valid = False
                flash("Your two password inputs are not the same.", category="error")

            # Username uniqueness check:
            # Queries the 'Users' table for usernames matching that of the user-inputted username.
            # '.first()' means that the 1st match will be outputted...
            # ...but, since, there cannot be more than 1 match anyway, this is completely fine
            username_matches = Users.query.filter_by(username=username).first()
            # If there is a match (ie: an account corresponding to the inputted username)
            if username_matches:
                valid = False
                flash("Username already exists.", category="error")

            if valid:
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

                # Stupid error fixed: 'User.password' -> 'username_match.password'.
                # Attempting to directly compare a string to an SQL table field, as expected, did not work.

                # DONE: Fix error when comparing hashed passwords.
                # When hashing the password for registration and login, a different salt is being used to salt the hash.
                # Therefore, the hashed password in the database will never match the user-inputted hashed password.

                # FIX: After reading the documentation of 'werkzeug.security', I realised that the parameters that...
                # ...must be passed are the hashed password (stored in the DB) and the PLAINTEXT password (user input).
                # Therefore, check_password_hash(hashed_password, username_match.password) becomes...
                # check_password_hash(username_match.password, password) for proper validation.
                # Lo and behold, the code works now and redirects users to the simulation page if their login...
                # ...details are correct

                if check_password_hash(username_match.password, password):
                    # 'remember=True' means that a logged-in user will stay logged in until they clear their browsing...
                    # ...data. Not part of the success criteria but a nice QoL feature.
                    # Feature addition approved by client after discussion.
                    login_user(username_match, remember=True)
                    return redirect(url_for('views.simulation'))
                else:
                    flash(message="Incorrect password.", category="error")
            else:
                flash("Username does not exist.", category="error")

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.root"))


@auth.route('/simulation')
def simulation():
    return render_template("simulation.html")
