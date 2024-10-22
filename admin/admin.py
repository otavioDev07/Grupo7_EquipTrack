from flask import render_template, Blueprint, request
from database.conection import *

admin_blueprint = Blueprint('admin', __name__, template_folder="templates")

@admin_blueprint.route('/cadastroEPI', methods=['GET','POST'])
def cadastro_EPI():
    if request.method == 'GET':
        #1 SELECT PARA PUXAR OS SETORES
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT * FROM setor')
            setores = cursor.fetchall()
            return render_template('cadastroEPI.html',setores=setores)
    
    if request.method == 'POST':
        nome = request.form['nome']
        numero-serie = request.form['numero-serie']


@admin_blueprint.route('/cadastroFuncionario')
def cadastro_Funcionario():
    return render_template('cadastroFuncionario.html')

@admin_blueprint.route('/descarte')
def descarte():
    return render_template('descarte.html')

@admin_blueprint.route('/cadastroDescarte')
def cadastroDescarte():
    return render_template('cadastroDescarte.html')

@admin_blueprint.route('/descricaoDescarte')
def descricaoDescarte():
    return render_template('descricaoDescarte.html')