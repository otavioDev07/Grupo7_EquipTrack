from flask import render_template, Blueprint, request, redirect, flash
from database.conection import conecta_db

alocar_blueprint = Blueprint('alocar', __name__, template_folder="templates", static_folder="static")

@alocar_blueprint.route('/alocar/<id>', methods=['GET', 'POST'])
def alocar_equipamento(id):
    if request.method == 'GET':
        # Carregar dados dos funcionários e do equipamento usando o id do EPI
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT idFuncionario, nomeFuncionário FROM funcionário WHERE idSetor = (SELECT idSetor FROM epi WHERE idEPI = %s)', (id,))
            funcionarios = cursor.fetchall()
            
            cursor.execute('SELECT nomeEquipamento, quantidade FROM epi WHERE idEPI = %s', (id,))
            equipamento = cursor.fetchall()
            
            return render_template('alocar.html', funcionarios=funcionarios, equipamento=equipamento, id=id)

    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                # Capturar dados do formulário
                idFuncionario = request.form['idFuncionario']
                quantidade = int(request.form['quantidade'])

                # Verificar a quantidade disponível
                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (id,))
                resultado = cursor.fetchone()

                if resultado is None:
                    flash('Equipamento não encontrado.', 'error')
                    return redirect(request.url)

                quantidade_disponivel = resultado[0]

                if quantidade > quantidade_disponivel:
                    flash('Quantidade solicitada excede a quantidade disponível.', 'error')
                    return redirect(request.url)

                # Atualizar quantidade do equipamento e registrar a alocação
                nova_quantidade = quantidade_disponivel - quantidade
                cursor.execute('UPDATE epi SET quantidade = %s WHERE idEPI = %s', (nova_quantidade, id))

                dataAlocacao = request.form['dataAlocacao']
                cursor.execute(
                    'INSERT INTO epi_funcionário (idEquipamento, idFuncionario, dataHora, quantidade) VALUES (%s, %s, %s, %s)',
                    (id, idFuncionario, dataAlocacao, quantidade)
                )
                conexao.commit()

                flash('Equipamento alocado com sucesso!', 'success')
                return redirect('/')

            except Exception as e:
                flash(f'Erro ao alocar equipamento: {str(e)}', 'error')
                return redirect(request.url)