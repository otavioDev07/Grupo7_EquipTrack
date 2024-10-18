from flask import render_template, Blueprint

admin_blueprint = Blueprint('admin', __name__, template_folder="templates")

@admin_blueprint.route('/cadastroEPI')
def cadastro_EPI():
    return render_template('cadastroEPI.html')

@admin_blueprint.route('/cadastroFuncionario')
def cadastro_Funcionario():
    return render_template('cadastroFuncionario.html')

@admin_blueprint.route('/descarte')
def descarte():
    return render_template('descarte.html')

@admin_blueprint.route('/cadastroDescarte')
def cadastroDescarte():
    return render_template('cadastroDescarte.html')