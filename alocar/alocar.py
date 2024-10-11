from flask import render_template, Blueprint

alocar_blueprint = Blueprint('alocar', __name__, template_folder="templates", static_folder="static")

@alocar_blueprint.route('/alocar')
def alocar():
    return render_template('alocar.html')
