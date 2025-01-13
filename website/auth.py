"""
As the file name suggests, all authentication rules will be established here.
"""
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If the webpage intends to send data
    if request.method == 'POST':
        # Data from the form in 'static/templates/login.html'
        login_or_register = request.form.get('logInOrRegister')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # User input validation for account creation/registration. The rules are:
        # - Username must be unique
        # - Length of username <= 16 characters
        # - Password must be at least 8 characters
        # - 'password' must be identical to 'confirm_password'
        if login_or_register == "register":
            if len(username) == 0 or len(password) == 0 or len(confirm_password) == 0:
                flash("One or more input fields are empty.", category="error")

            elif len(username) > 16:
                flash("Your username cannot be greater than 16 characters.", category="error")

            elif len(password) < 8:
                flash("Your password cannot be less than 8 characters.", category="error")

            elif password != confirm_password:
                flash("Your two password inputs are not the same.", category="error")

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
