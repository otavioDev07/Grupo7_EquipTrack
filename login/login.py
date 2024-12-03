from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from database.conection import conecta_db

login_blueprint = Blueprint('login', __name__, template_folder="templates")

@login_blueprint.route('/')
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()    
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        password = request.form.get('password')

        if not cpf or not password:
            flash('CPF e senha são obrigatórios!', 'danger')
            return redirect(url_for('login.login'))

        with conecta_db() as (conexao, cursor):
            query = "SELECT idSupervisor, senhaAcesso FROM supervisor WHERE CPF = %s AND status = 'ativo'"
            cursor.execute(query, (cpf,))
            result = cursor.fetchone()

        if result:
            id_supervisor, hashed_password = result
            if check_password_hash(hashed_password, password):
                session['idSupervisor'] = id_supervisor 
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('home.home')) 
            else:
                flash('Senha incorreta!', 'danger')
        else:
            flash('CPF não encontrado ou conta inativa.', 'danger')

    return render_template('login.html')