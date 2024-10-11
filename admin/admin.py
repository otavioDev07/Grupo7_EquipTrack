from flask import render_template, Blueprint

admin_blueprint = Blueprint('admin', __name__, template_folder="templates")

@admin_blueprint.route('/cadastroEPI')
def cadastro_EPI():
    return render_template('cadastroEPI.html')