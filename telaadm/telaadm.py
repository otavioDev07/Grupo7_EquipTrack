from flask import Flask, Blueprint, render_template, request, redirect, session
from database.conection import conecta_db
from session.session  import require_login
from werkzeug.security import generate_password_hash, check_password_hash


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
            query = 'SELECT idSupervisor, nomeSupervisor, CPF, status, senhaAcesso FROM supervisor WHERE idSupervisor = %s'
            cursor.execute(query, (idSupervisor,))
            result = cursor.fetchall()

            if result:
                cipeiro = [
                    {
                        'idSupervisor': row[0],
                        'nomeSupervisor': row[1],
                        'CPF': row[2],
                        'status': row[3],
                        'senhaAcesso': row[4]
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

@telaadm_blueprint.route('/editarCipeiro/<int:idSupervisor>', methods=['GET', 'POST'])
@require_login
def editarCipeiro(idSupervisor):
    with conecta_db() as (conexao, cursor):
        # Se o método for GET, buscar os dados do supervisor para preencher o formulário
        if request.method == 'GET':
            try:
                # Consulta para obter os dados do supervisor
                query = 'SELECT idSupervisor, nomeSupervisor, CPF, status, senhaAcesso FROM supervisor WHERE idSupervisor = %s'
                cursor.execute(query, (idSupervisor,))
                result = cursor.fetchone()  # Usa fetchone para pegar apenas uma linha

                if result:
                    # Organize os dados em um dicionário para fácil acesso no template
                    cipeiro = {
                        'idSupervisor': result[0],
                        'nomeSupervisor': result[1],
                        'CPF': result[2],
                        'status': result[3],
                        'senhaAcesso': result[4]
                    }
                    return render_template('editarCipeiro.html', cipeiro=cipeiro)
                else:
                    return "Cipeiro não encontrado", 404
            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

        # Se o método for POST, salvar as edições
        if request.method == 'POST':
            try:
                # Pegando os dados do formulário de edição
                nome = request.form['nomeSupervisor']
                cpf = request.form['CPF']
                status = request.form['status']
                senhaAcesso = request.form['senhaAcesso']

                # Comando SQL para atualizar os dados do supervisor no banco
                comando = '''
                    UPDATE supervisor
                    SET nomeSupervisor = %s, CPF = %s, status = %s, senhaAcesso = %s
                    WHERE idSupervisor = %s
                '''
                cursor.execute(comando, (nome, cpf, status, senhaAcesso, idSupervisor))
                conexao.commit()

                # Após salvar, redirecionar de volta para os detalhes do supervisor
                return redirect(f'/detalhesCipeiro/{idSupervisor}')
            except Exception as e:
                return f"Erro ao salvar as edições: {e}", 500


if __name__ == '__main__':
    telaadm_blueprint.run(debug=True)


