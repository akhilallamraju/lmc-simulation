"""
As the file name suggests, all authentication rules will be established here.
"""
from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<h1>Logout Page</h1>"


@auth.route('/simulation')
def simulation():
    return render_template("simulation.html")
