from flask import render_template, Blueprint

login_blueprint = Blueprint('login', __name__, template_folder="templates", static_folder="static")