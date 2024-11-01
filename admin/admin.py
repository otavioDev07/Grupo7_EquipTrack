from flask import render_template, Blueprint, request, flash, redirect
from database.conection import *
from datetime import datetime

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
        with conecta_db() as (conexao, cursor):
            try:
                # Campos obrigatórios
                codigoCA = request.form['ca']
                numeroSerie = request.form['numero-serie']
                marca = request.form['marca']
                nomeEquipamento = request.form['nome']
                dataAquisicao = request.form['dataAquisicao']
                quantidade = request.form['quantidade']
                dataVencimento = request.form['dataVencimento']
                idSetor = request.form['idSetor'] #Verificar se o valor está vindo 
                idSupervisor = 1 #Virá através da autenticação (Não feito ainda)


                # Campos opcionais
                modelo = request.form.get('modelo')
                dataLocacao = None
                observacoes = request.form.get('observacoes')
                tamanho = request.form.get('tamanho')

                # Validação do campo `status`
                status = request.form['status']
                if status not in ["Em uso", "Estoque"]:
                    flash('Status inválido. Deve ser "Em uso" ou "Estoque".', 'error')
                    return redirect(request.url)

                # Validação das datas
                try:
                    dataVencimento = datetime.strptime(dataVencimento, '%Y-%m-%d').strftime('%Y/%m/%d')
                    dataAquisicao = datetime.strptime(dataAquisicao, '%Y-%m-%d').strftime('%Y/%m/%d')

                    if dataLocacao:
                        dataLocacao = datetime.strptime(dataLocacao, '%Y-%m-%d').strftime('%Y/%m/%d')
                except ValueError:
                    flash({'error': 'Formato de data inválido. Use o formato AAAA-MM-DD.'}), 400
                    return redirect(request.url)
                comando = '''
                    INSERT INTO EPI (codigoCA, numeroSerie, marca, modelo, dataLocacao, dataVencimento, status, observacoes, nomeEquipamento, dataAquisicao, tamanho, quantidade, idSetor) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(comando, (codigoCA, numeroSerie, marca, modelo, dataLocacao, dataVencimento, status, observacoes, nomeEquipamento, dataAquisicao, tamanho, quantidade, idSetor))
                conexao.commit()

                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Cadastro de EPI: {nomeEquipamento}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect('/cadastroEPI')
            except Exception as e:
                flash(f'Erro: {str(e)}', 'error')
                return redirect(request.url)


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

@admin_blueprint.route('/descricaoEPI')
def descricaoEPI():
    return render_template('descricaoEPI.html')

@admin_blueprint.route('/atividadeMensal')
def atividadeMensal():
    return render_template('atividadeMensal.html')

@admin_blueprint.route('/edicaoEPI')
def edicaoEPI():
    return render_template('edicaoEPI.html')

@admin_blueprint.route('/edicaoFuncionario')
def edicaoFuncionario():
    return render_template('edicaoFuncionario.html')

@admin_blueprint.route('/descricaoFuncionario')
def descricaoFuncionario():
    return render_template('descricaoFuncionario.html')