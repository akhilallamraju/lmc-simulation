"""
This file defines the web application's structure, establishing all the paths/routes (called views) within the site.
These views are stored in a special object called a blueprint.
"""
# 'Blueprint' allows for the use of blueprint objects.
# 'render_template' allows Jinja templates to be displayed/rendered.
from flask import Blueprint, render_template, request, send_file, flash
from flask_login import current_user
import csv
import os

from unicodedata import category

views = Blueprint('views', __name__)  # This will hold all the URLs for the pages within the web app


# The root route, where the user will end up when the website's URL is entered.
@views.route('/')
# This function is run when a user enters the root page.
def root():
    return render_template("root.html")


@views.route('/simulation', methods=['GET', 'POST'])
def simulation():
    # 'is_authenticated' will be set to True only if the user has successfully logged in.
    if current_user.is_authenticated:
        return render_template("simulation-logged-in.html", user=current_user)

    else:
        return render_template("simulation.html")


@views.route('/receive-code', methods=['POST'])
def receive_code():
    # Receives the JSON object sent from index.js
    data = request.get_json()

    code_as_2d_list = data['code']

    with open(f"instance/code/{current_user.get_id()}.csv", "w+") as file:
        writer = csv.writer(file)
        writer.writerow(["label", "opcode", "operand"])
        writer.writerows(code_as_2d_list)

    return render_template("simulation-logged-in.html", user=current_user)


@views.route('/download-code')
def download_code():
    directory = f"{os.getcwd()}/instance/code/{current_user.get_id()}.csv"

    if os.path.exists(directory):
        return send_file(directory, as_attachment=True)

    # If the user does not have a file saved, an appropriate error message is outputted
    flash(message="You do not have a file saved", category="download-error")
    return render_template("simulation-logged-in.html", user=current_user)

