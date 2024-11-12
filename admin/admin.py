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
                    print('Formato de data inválido. Use o formato AAAA-MM-DD.')
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


@admin_blueprint.route('/cadastroFuncionario', methods=['GET','POST'])
def cadastro_Funcionario():
    if request.method == 'GET':
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT * FROM setor')
            setores = cursor.fetchall()
            return render_template('cadastroFuncionario.html',setores=setores)
    
    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                nome = request.form['nome']
                nif = request.form['nif']
                cpf = request.form['cpf']
                cargo = request.form['cargo']
                idSetor = request.form['idSetor']
                roupa = request.form['tamanhoRoupa']
                calcados = request.form['calcados']
                especial = request.form.get('condicoesEspeciais')
                idSupervisor = 2 #Virá através da autenticação (Não feito ainda)
                print('CHEGOU AQUI')
                comando = '''
                    INSERT INTO funcionário (nomeFuncionário, NIF, CPF, idSetor, condicoesEspeciais, cargo, tamCalcado, tamRoupa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(comando, (nome, nif, cpf, idSetor, especial, cargo, calcados, roupa))
                conexao.commit()

                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Cadastro de funcionário: {nome}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()

                print('Cadastro realizado com sucesso!', 'success')
                return redirect('/')

            except Exception as e:
                return f"Erro de BackEnd: {e}"
            except Error as e:
                return f"Erro de BD:{e}"
                

@admin_blueprint.route('/descarte')
def descarte():
    query = 'SELECT e.idEPI, e.codigoCA, e.nomeEquipamento, e.quantidade FROM epi e INNER JOIN descarte d ON d.idEquipamento = e.idEPI'
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute(query)
            EPIs = cursor.fetchall()
            return render_template('descarte.html', EPIs=EPIs)
    except Exception as e:
        print("Erro ao buscar dados:", e)
        return "Erro ao buscar dados", 500
    
@admin_blueprint.route('/descricaoDescarte/<int:idEPI>', methods=['GET'])
def descricaoDescarte(idEPI):
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT * FROM epi WHERE idEPI = %s', (idEPI,))
            epi = cursor.fetchone()

            cursor.execute('SELECT se.nomeSetor FROM setor se INNER JOIN epi ep ON se.idSetor = ep.idSetor WHERE idEPI = %s', (idEPI,))
            nomeSetor = cursor.fetchone()

            cursor.execute('SELECT f.nomeFuncionário FROM funcionário f INNER JOIN epi e ON f.idFuncionario = e.idFuncionario WHERE e.idEPI = %s', (idEPI,))
            nomeFuncionário = cursor.fetchone()[0] 

            cursor.execute('SELECT * FROM descarte WHERE idEquipamento = %s', (idEPI,))
            descarte = cursor.fetchone()

            if epi and nomeFuncionário and descarte:
                epi = {
                    'idEPI': epi[0],
                    'codigoCA': epi[1],
                    'numeroSerie': epi[2],
                    'marca': epi[3],
                    'modelo': epi[4],
                    'dataLocacao': epi[5],
                    'dataVencimento': epi[6],
                    'status': epi[7],
                    'observacoes': epi[8],
                    'nomeEquipamento': epi[9],
                    'dataAquisicao': epi[10],
                    'tamanho': epi[11],
                    'quantidade': epi[12],
                    'nomeSetor': nomeSetor
                }

                descarte = {
                    'quantidade': descarte[5],
                    'motivoDescarte': descarte[1],
                    'localDescarte': descarte[2],
                    'dataDescarte': descarte[3]
                }
                return render_template('descricaoDescarte.html', epi=epi, descarte=descarte, nomeFuncionário=nomeFuncionário)
            else:
                return "EPI não encontrado", 404
    except Exception as e:
        return f"Ocorreu um erro: {e}", 500
        
@admin_blueprint.route('/cadastroDescarte/<int:idEPI>', methods=['GET','POST'])
def cadastroDescarte(idEPI):
    if request.method == 'GET':
        with conecta_db() as (conexao, cursor):
            try:
                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (idEPI,))
                quantidade = cursor.fetchone()[0]
            except Exception as e:
                return f"Erro de BackEnd: {e}"
            return render_template('cadastroDescarte.html', quantidade=quantidade)
        
    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                motivo = request.form('motivoDescarte')
                localDescarte = request.form('localDescarte')
                idSupervisor = 2 #Virá através da autenticação (Não feito ainda)

                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (idEPI,))
                quantidade = cursor.fetchone()[0]

                comando = f'INSERT INTO descarte (motivoDescarte, localDescarte, dataDescarte, idEquipamento, quantidade) VALUES (%s, %s, NOW(), %s, %s)'
                cursor.execute(comando, (motivo, localDescarte, idEPI, quantidade))
                conexao.commit()

                cursor.execute('SELECT nomeEquipamento FROM epi WHERE idEPI = %s', (idEPI,))
                nomeEPI = cursor.fetchone()[0]

                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Descarte de EPI: {nomeEPI}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()

            except Exception as e:
                return f"Erro de BackEnd: {e}"
            

@admin_blueprint.route('/editDescarte/<int:idEPI>', methods=['GET', 'POST'])
def editDescarte(idEPI):
    pass

@admin_blueprint.route('/descricaoEPI/<int:idEPI>', methods=['GET'])
def descricaoEPI(idEPI):
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute('SELECT * FROM epi WHERE idEPI = %s', (idEPI,))
            result = cursor.fetchone()

            cursor.execute('SELECT f.nomeFuncionário FROM funcionário f INNER JOIN epi ep ON f.idFuncionario = ep.idFuncionario WHERE idEPI = %s', (idEPI,))
            nomeColaborador = cursor.fetchone()

            cursor.execute('SELECT se.nomeSetor FROM setor se INNER JOIN epi ep ON se.idSetor = ep.idSetor WHERE idEPI = %s', (idEPI,))
            nomeSetor = cursor.fetchone()

            if result:
                epi = {
                    'idEPI': result[0],
                    'codigoCA': result[1],
                    'numeroSerie': result[2],
                    'marca': result[3],
                    'modelo': result[4],
                    'dataLocacao': result[5],
                    'dataVencimento': result[6],
                    'status': result[7],
                    'observacoes': result[8],
                    'nomeEquipamento': result[9],
                    'dataAquisicao': result[10],
                    'tamanho': result[11],
                    'quantidade': result[12],
                    'nomeSetor': nomeSetor,
                    'nomeColaborador': nomeColaborador
                }
                return render_template('descricaoEPI.html', epi=epi)
            else:
                return "EPI não encontrado", 404

        except Exception as e:
            return f"Erro de BackEnd: {e}"
    