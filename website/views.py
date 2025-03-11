"""
This file defines the web application's structure, establishing all the paths/routes (called views) within the site.
These views are stored in a special object called a blueprint.
"""
# 'Blueprint' allows for the use of blueprint objects.
# 'render_template' allows Jinja templates to be displayed/rendered.
from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)  # This will hold all the URLs for the pages within the web app


# The root route, where the user will end up when the website's URL is entered.
@views.route('/')
# This function is run when a user enters the root page.
def root():
    return render_template("root.html")


@views.route('/simulation')
def simulation():
    # 'is_authenticated' will be set to True only if the user has successfully logged in.
    if current_user.is_authenticated:
        return render_template("simulation-logged-in.html", user=current_user)
    else:
        return render_template("simulation.html")
