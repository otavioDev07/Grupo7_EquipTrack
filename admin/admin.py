from flask import render_template, Blueprint, request, flash, redirect
from database.conection import *
from datetime import datetime
from mysql.connector import Error

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
                idSupervisor = 2 #Virá através da autenticação (Não feito ainda)

                # Campos opcionais
                modelo = request.form.get('modelo')
                observacoes = request.form.get('observacoes')
                tamanho = request.form.get('tamanho')

                
                status = 'Estoque'

                # Validação das datas
                try:
                    dataVencimento = datetime.strptime(dataVencimento, '%Y-%m-%d').strftime('%Y/%m/%d')
                    dataAquisicao = datetime.strptime(dataAquisicao, '%Y-%m-%d').strftime('%Y/%m/%d')
                except ValueError:
                    flash({'error': 'Formato de data inválido. Use o formato AAAA-MM-DD.'}), 400
                    return redirect(request.url)
                comando = '''
                    INSERT INTO EPI (codigoCA, numeroSerie, marca, modelo, dataVencimento, status, observacoes, nomeEquipamento, dataAquisicao, tamanho, quantidade, idSetor) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(comando, (codigoCA, numeroSerie, marca, modelo, dataVencimento, status, observacoes, nomeEquipamento, dataAquisicao, tamanho, quantidade, idSetor))
                conexao.commit()
        
                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Cadastro de EPI: {nomeEquipamento}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()
                print('Cadastro realizado com sucesso!', 'success')
                return redirect('/')
            except Exception as e:
                return f"Erro de BackEnd: {e}"
            except Error as e:
                return f"Erro de BD:{e}"


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