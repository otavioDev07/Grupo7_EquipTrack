from flask import render_template, Blueprint, request, redirect, session
from session.session import require_login
from database.conection import conecta_db

alocar_blueprint = Blueprint('alocar', __name__, template_folder="templates", static_folder="static")

@alocar_blueprint.route('/alocar/<int:idEPI>', methods=['GET', 'POST'])
@require_login
def alocar_equipamento(idEPI):
    if request.method == 'GET':
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT idFuncionario, nomeFuncionário FROM funcionário WHERE idSetor = (SELECT idSetor FROM epi WHERE idEPI = %s)', (idEPI,))
            funcionarios = cursor.fetchall()
            
            cursor.execute('SELECT nomeEquipamento, quantidade FROM epi WHERE idEPI = %s', (idEPI,))
            equipamento = cursor.fetchall()
            
            return render_template('alocar.html', funcionarios=funcionarios, equipamento=equipamento, idEPI=idEPI)

    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                idFuncionario = request.form['idFuncionario']
                quantidade = int(request.form['quantidade'])
                idSupervisor = session['idSupervisor']

                comando = 'INSERT INTO epi_funcionário (idEquipamento, idFuncionario, dataHora, quantidade) VALUES (%s, %s, NOW(), %s)'
                cursor.execute(comando, (idEPI, idFuncionario, quantidade))
                conexao.commit()

                atualizar_epi = 'UPDATE epi SET quantidade = quantidade - %s, idFuncionario = %s, status = %s WHERE idEPI = %s'
                cursor.execute(atualizar_epi, (quantidade, idFuncionario,'Em uso', idEPI))
                conexao.commit()    

                #backlog
                cursor.execute('SELECT nomeFuncionário FROM funcionário WHERE idFuncionario = %s', (idFuncionario,))
                funcionario = cursor.fetchone()[0]

                cursor.execute('SELECT nomeEquipamento FROM epi WHERE idEPI = %s', (idEPI,))
                equipamento = cursor.fetchone()[0]

                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Locação de EPI: {equipamento} para colaborador {funcionario}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()
                print('Cadastro realizado com sucesso!', 'success')
                return redirect('/estoque')
            except Exception as e:
                conexao.rollback()
                print(f'Erro ao alocar equipamento: {str(e)}', 'error')
                return redirect(request.url)