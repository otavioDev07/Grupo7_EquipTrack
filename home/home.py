from flask import render_template, Blueprint

home_blueprint = Blueprint('home', __name__, template_folder="templates")

@home_blueprint.route('/')
@home_blueprint.route('/home')
def home():
    return render_template('home.html')

@home_blueprint.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')