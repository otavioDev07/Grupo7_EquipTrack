from flask import Flask, Blueprint, render_template, request, redirect, session
from database.conection import conecta_db
from session.session  import require_login
from werkzeug.security import generate_password_hash


telaadm_blueprint = Blueprint('telaadm', __name__, template_folder="templates")

@telaadm_blueprint.route('/telaadm', methods=['GET'])
@require_login
def telaadm(): 
    with conecta_db() as (conexao, cursor):
        try:
            query = 'SELECT idSupervisor, nomeSupervisor, CPF, status FROM supervisor'
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                cipeiros = [
                {
                    'idSupervisor': row[0],
                    'nomeSupervisor': row[1],
                    'CPF': row[2],
                    'status': row[3]
                }
                for row in result
            ]
            return render_template('verCipeiros.html', cipeiros=cipeiros)
        except Exception as e:
            return f"Erro de BackEnd: {e}", 500

@telaadm_blueprint.route('/detalhesCipeiro/<int:idSupervisor>', methods=['GET'])
@require_login
def detalhesCipeiro(idSupervisor):
    with conecta_db() as (conexao, cursor):
        try:
            query = 'SELECT idSupervisor, nomeSupervisor, CPF, status FROM supervisor WHERE idSupervisor = %s'
            cursor.execute(query, (idSupervisor,))
            result = cursor.fetchall()

            if result:
                cipeiro = [
                    {
                        'idSupervisor': row[0],
                        'nomeSupervisor': row[1],
                        'CPF': row[2],
                        'status': row[3]
                    }
                    for row in result
                ]
                return render_template('detalhesCipeiro.html', cipeiro=cipeiro)
            else:
                return "Nenhum CIPEIRO encontrado.", 404
        except Exception as e:
            return f"Erro de BackEnd: {e}", 500
        
@telaadm_blueprint.route('/cadastrarCipeiro', methods=['GET', 'POST'])
@require_login
def cadastrarCipeiro():
    if request.method == 'GET':
        return render_template('cadastroCipeiro.html')

    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                nomeSupervisor = request.form['nomeSupervisor']
                cpf = request.form['CPF']
                senha = request.form['senhaAcesso']
                senha_cript = generate_password_hash(senha)
                idSupervisor = session['idSupervisor']

                query = 'INSERT INTO supervisor (nomeSupervisor, CPF, senhaAcesso) VALUES (%s, %s, %s)'
                cursor.execute(query, (nomeSupervisor, cpf, senha_cript))
                conexao.commit()

                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Cadastro de supervisor: {nomeSupervisor}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()
                
                return redirect('/home')
            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

@telaadm_blueprint.route('/editarCipeiro/<int:idSupervisor>', methods=['GET', 'PUT'])
@require_login
def editarCipeiro(idSupervisor):
    with conecta_db() as (conexao, cursor):
        if request.method == 'GET':
            try:
                query = 'SELECT idSupervisor, nomeSupervisor, CPF, status FROM supervisor WHERE idSupervisor = %s'
                cursor.execute(query, (idSupervisor,))
                result = cursor.fetchone()  

                if result:
                    cipeiro = {
                        'idSupervisor': result[0],
                        'nomeSupervisor': result[1],
                        'CPF': result[2],
                        'status': result[3]
                    }
                    return render_template('editarCipeiro.html', cipeiro=cipeiro)
                else:
                    return "Cipeiro não encontrado", 404
            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

        if request.method == 'PUT':
            try:
                nome = request.form['nomeSupervisor']
                cpf = request.form['CPF']
                status = request.form['status']
                senhaAcesso = request.form['senhaAcesso']
                senha_cript = generate_password_hash(senhaAcesso)

                comando = '''
                    UPDATE supervisor
                    SET nomeSupervisor = %s, CPF = %s, status = %s, senhaAcesso = %s
                    WHERE idSupervisor = %s
                '''
                cursor.execute(comando, (nome, cpf, status, senha_cript, idSupervisor))
                conexao.commit()

                return redirect(f'/detalhesCipeiro/{idSupervisor}')
            except Exception as e:
                return f"Erro ao salvar as edições: {e}", 500


if __name__ == '__main__':
    telaadm_blueprint.run(debug=True)


