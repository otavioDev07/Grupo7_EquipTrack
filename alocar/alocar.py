from flask import render_template, Blueprint, request, redirect, flash
from database.conection import conecta_db

alocar_blueprint = Blueprint('alocar', __name__, template_folder="templates", static_folder="static")

@alocar_blueprint.route('/alocar/<int:idEPI>', methods=['GET', 'POST'])
def alocar_equipamento(idEPI):
    if request.method == 'GET':
        # Selecionar funcionários e equipamentos disponíveis
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT idFuncionario, nomeFuncionário FROM funcionário')
            funcionarios = cursor.fetchall()
            
            cursor.execute('SELECT idEPI, nomeEquipamento, quantidade FROM epi WHERE status = "Estoque"')
            equipamentos = cursor.fetchall()
            
            return render_template('alocar.html', funcionarios=funcionarios, equipamentos=equipamentos)

    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                # Capturar os dados do formulário
                idFuncionario = request.form['idFuncionario']
                idEPI = request.form['idEPI']
                quantidade = int(request.form['quantidade'])  # Convertendo para inteiro

                # Verificar se a quantidade solicitada está disponível
                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (idEPI,))
                resultado = cursor.fetchone()

                if resultado is None:
                    flash('Equipamento não encontrado.', 'error')
                    return redirect(request.url)

                quantidade_disponivel = resultado[0]

                if quantidade > quantidade_disponivel:
                    flash('Quantidade solicitada excede a quantidade disponível.', 'error')
                    return redirect(request.url)

                # Atualizar a quantidade do equipamento
                nova_quantidade = quantidade_disponivel - quantidade
                cursor.execute('UPDATE epi SET quantidade = %s WHERE idEPI = %s', (nova_quantidade, idEPI))

                # Inserir na tabela de alocação
                dataAlocacao = request.form['dataAlocacao']
                comando = '''
                    INSERT INTO epi_funcionário (idEquipamento, idFuncionario, dataHora, quantidade) 
                    VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(comando, (idEPI, idFuncionario, dataAlocacao, quantidade))
                conexao.commit()

                flash('Equipamento alocado com sucesso!', 'success')
                return redirect('/alocar')
            except Exception as e:
                flash(f'Erro ao alocar equipamento: {str(e)}', 'error')
                return redirect(request.url)
