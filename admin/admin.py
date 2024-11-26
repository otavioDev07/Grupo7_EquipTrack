from flask import render_template, Blueprint, request, redirect
from database.conection import *
from datetime import datetime
from datetime import date
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
                idSupervisor = 1 #Virá através da autenticação (Não feito ainda)

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
                idSupervisor = 1 #Virá através da autenticação (Não feito ainda)
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
    query = 'SELECT e.idEPI, e.codigoCA, e.nomeEquipamento, d.quantidade FROM epi e INNER JOIN descarte d ON d.idEquipamento = e.idEPI'
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
            nomeSetor = cursor.fetchone()[0]

            cursor.execute('SELECT * FROM descarte WHERE idEquipamento = %s', (idEPI,))
            descarte = cursor.fetchone()

            if epi and descarte:
                epi = {
                    'idEPI': epi[0],
                    'codigoCA': epi[1],
                    'numeroSerie': epi[2],
                    'marca': epi[3],
                    'modelo': epi[4],
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
                return render_template('descricaoDescarte.html', epi=epi, descarte=descarte)
            else:
                return "EPI não encontrado", 404
    except Exception as e:
        return f"Ocorreu um erro: {e}", 500
        
@admin_blueprint.route('/cadastroDescarte/<int:idEPI>', methods=['GET', 'POST'])
def cadastroDescarte(idEPI):
    with conecta_db() as (conexao, cursor):
        if request.method == 'GET':
            try:
                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (idEPI,))
                result = cursor.fetchone()
                if result:
                    quantidade = result[0]
                else:
                    return "Erro: EPI não encontrado.", 404
            except Exception as e:
                return f"Erro de BackEnd: {e}"
            
            return render_template('cadastroDescarte.html', quantidade=quantidade, idEPI=idEPI)
        
        elif request.method == 'POST':
            try:
                quantidade_descartar = int(request.form['quantidade'])
                motivo = request.form['motivoDescarte']
                localDescarte = request.form['localDescarte']
                idSupervisor = 1  

                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (idEPI,))
                result = cursor.fetchone()
                if result:
                    quantidade_atual = result[0]
                else:
                    return "Erro: EPI não encontrado.", 404

                if quantidade_atual <= 0:
                    return "Erro: Não há quantidade disponível para descarte.", 400
                elif quantidade_descartar > quantidade_atual:
                    return "Erro: Quantidade a ser descartada excede a quantidade disponível.", 400

                comando = '''
                    INSERT INTO descarte (motivoDescarte, localDescarte, dataDescarte, idEquipamento, quantidade)
                    VALUES (%s, %s, NOW(), %s, %s)
                '''
                cursor.execute(comando, (motivo, localDescarte, idEPI, quantidade_descartar))
                conexao.commit()

                comando_update = 'UPDATE epi SET quantidade = quantidade - %s WHERE idEPI = %s'
                cursor.execute(comando_update, (quantidade_descartar, idEPI))
                conexao.commit()

                cursor.execute('SELECT nomeEquipamento FROM epi WHERE idEPI = %s', (idEPI,))
                result = cursor.fetchone()
                if result:
                    nomeEPI = result[0]
                else:
                    nomeEPI = "Desconhecido"
                    
                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Descarte de EPI: {nomeEPI}"
                cursor.execute(comando_backlog, (acao, idSupervisor))
                conexao.commit()

                # Redireciona para a página de estoque após o sucesso
                return redirect('/estoque')

            except Exception as e:
                return f"Erro de BackEnd: {e}", 500
            

@admin_blueprint.route('/editDescarte/<int:idEPI>', methods=['GET', 'POST'])
def editDescarte(idEPI):
    pass

@admin_blueprint.route('/descricaoEPI/<int:idEPI>', methods=['GET'])
def descricaoEPI(idEPI):
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute('SELECT * FROM epi WHERE idEPI = %s', (idEPI,))
            result = cursor.fetchone()

            cursor.execute('SELECT se.nomeSetor FROM setor se INNER JOIN epi ep ON se.idSetor = ep.idSetor WHERE idEPI = %s', (idEPI,))
            nomeSetor = cursor.fetchone()

            if result:
                epi = {
                    'idEPI': result[0],
                    'codigoCA': result[1],
                    'numeroSerie': result[2],
                    'marca': result[3],
                    'modelo': result[4],
                    'dataVencimento': result[6],
                    'status': result[7],
                    'observacoes': result[8],
                    'nomeEquipamento': result[9],
                    'dataAquisicao': result[10],
                    'tamanho': result[11],
                    'quantidade': result[12],
                    'nomeSetor': nomeSetor
                }
                return render_template('descricaoEPI.html', epi=epi)
            else:
                return "EPI não encontrado", 404

        except Exception as e:
            return f"Erro de BackEnd: {e}"
            
        
@admin_blueprint.route('/funcionarios/<int:idSetor>', methods=['GET'])
def get_funcionarios(idSetor):
    try:
        with conecta_db() as (conexao, cursor):
            # Consulta para buscar todos os funcionários do setor
            cursor.execute('SELECT idFuncionario, nomeFuncionário, NIF, cargo FROM funcionário WHERE idSetor = %s', (idSetor,))
            funcionarios = cursor.fetchall() 

            # Consulta para buscar o nome do setor
            cursor.execute('SELECT nomeSetor FROM setor WHERE idSetor = %s', (idSetor,))
            nomeSetor = cursor.fetchone() 

            # Verifica se os dados foram encontrados
            if not nomeSetor:
                return 'Setor não encontrado', 404

            if not funcionarios:
                return 'Funcionários não encontrados', 404
            
            lista_funcionarios = [
                {
                    'idFuncionario': funcionario[0],
                    'nomeFuncionario': funcionario[1],
                    'NIF': funcionario[2],
                    'cargo': funcionario[3]
                }
                for funcionario in funcionarios
            ]

            return render_template('funcionarios.html', funcionario=lista_funcionarios, nomeSetor=nomeSetor[0])

    except Exception as e:
        return f"Erro de BackEnd: {e}", 500
    

@admin_blueprint.route('/descFuncionario/<int:idFuncionario>', methods=['GET'])
def descFuncionario(idFuncionario):
    try:
        with conecta_db() as (conexao, cursor):
            # Busca os dados do funcionário
            comando_funcionario = '''
                SELECT f.idFuncionario, f.nomeFuncionário, f.NIF, f.cargo, f.condicoesEspeciais, f.tamCalcado, f.tamRoupa, s.nomeSetor
                FROM funcionário f
                INNER JOIN setor s ON f.idSetor = s.idSetor
                WHERE f.idFuncionario = %s
            '''
            cursor.execute(comando_funcionario, (idFuncionario,))
            dados = cursor.fetchone()

            if not dados:
                return "Funcionário não encontrado", 404

            funcionario = {
                'idFuncionario': dados[0],
                'nomeFuncionario': dados[1],
                'NIF': dados[2],
                'cargo': dados[3],
                'condicoesEspeciais': dados[4],
                'tamCalcado': dados[5],
                'tamRoupa': dados[6],
                'nomeSetor': dados[7]
            }

            comando_epis = '''
                SELECT e.idEPI, e.codigoCA, e.nomeEquipamento, e.dataVencimento, ef.idEPI_Funcionario
                FROM epi e
                INNER JOIN epi_funcionário ef ON e.idEPI = ef.idEquipamento
                WHERE ef.idFuncionario = %s AND e.status != "Descartado"
            '''
            cursor.execute(comando_epis, (idFuncionario,))
            EPIs = cursor.fetchall()

            lista_epis = [
                {
                    'idEPI': epi[0],
                    'codigoCA': epi[1],
                    'nomeEquipamento': epi[2],
                    'dataVencimento': epi[3],
                    'idEPI_Funcionario': epi[4]
                }
                for epi in EPIs
            ]

            now = date.today()

        return render_template('descricaoFuncionario.html', funcionario=funcionario, EPIs=lista_epis, now=now)
    
    except Exception as e:
        return f"Erro: {str(e)}", 500
    

@admin_blueprint.route('/epiFuncionario/<int:id>', methods=['GET'])
def epi_funcionario(id):
    try:
        with conecta_db() as (conexao, cursor):
            comando = '''
                SELECT 
                    e.idEPI,
                    e.codigoCA,
                    e.numeroSerie,
                    e.marca,
                    e.modelo,
                    ef.dataHora,
                    e.dataVencimento,
                    e.observacoes,
                    e.nomeEquipamento,
                    e.dataAquisicao,
                    e.tamanho,
                    ef.quantidade,
                    s.nomeSetor,
                    f.nomeFuncionário
                FROM epi_funcionário ef
                INNER JOIN epi e ON ef.idEquipamento = e.idEPI
                INNER JOIN funcionário f ON ef.idFuncionario = f.idFuncionario
                INNER JOIN setor s ON f.idSetor = s.idSetor
                WHERE ef.idEPI_Funcionario = %s
            '''
            cursor.execute(comando, (id,))
            dados = cursor.fetchone()

            if not dados:
                return "EPI ou Funcionário não encontrado", 404

            epi = {
                'idEPI': dados[0],
                'codigoCA': dados[1],
                'numeroSerie': dados[2],
                'marca': dados[3],
                'modelo': dados[4],
                'dataHora': dados[5],
                'dataVencimento': dados[6],
                'observacoes': dados[7],
                'nomeEquipamento': dados[8],
                'dataAquisicao': dados[9],
                'tamanho': dados[10],
                'quantidade': dados[11],
                'nomeSetor': dados[12],
                'nomeFuncionario': dados[13],
                'idEPI_Funcionario':id
            }

        return render_template('epiFuncionario.html', epi=epi)

    except Exception as e:
        print(f"Erro ao buscar dados do EPI alocado: {e}")
        return "Erro ao buscar dados", 500

@admin_blueprint.route('/DescarteEPIalocado/<int:id>', methods=['GET', 'POST'])
def descarteEPI_alocado(id):
    with conecta_db() as (conexao, cursor):
        if request.method == 'GET':
            try:
                cursor.execute('SELECT quantidade FROM epi_funcionário WHERE idEPI_Funcionario = %s', (id,))
                quantidade = cursor.fetchone()[0]
            except Exception as e:
                return f"Erro de BackEnd: {e}"
            return render_template('cadastroDescarteFuncionario.html', quantidade=quantidade, idEPI=id)

        if request.method == 'POST':
            try:
                cursor.execute('SELECT quantidade FROM epi_funcionário WHERE idEPI_Funcionario = %s', (id,))
                quantidade_atual = cursor.fetchone()[0]

                quantidade_descartar = int(request.form['quantidade'])
                motivo = request.form['motivoDescarte']
                localDescarte = request.form['localDescarte']
                idSupervisor = 1  

                if quantidade_atual <= 0:
                    return "Erro: Não há quantidade disponível para descarte.", 400
                elif quantidade_descartar > quantidade_atual:
                    return "Erro: Quantidade a ser descartada excede a quantidade disponível.", 400

                cursor.execute('SELECT idEquipamento FROM epi_funcionário WHERE idEPI_Funcionario = %s', (id,))
                idEPI = cursor.fetchone()[0]

                comando_inserir_descarte = '''
                    INSERT INTO descarte (motivoDescarte, localDescarte, dataDescarte, idEquipamento, quantidade)
                    VALUES (%s, %s, NOW(), %s, %s)
                ''' 
                cursor.execute(comando_inserir_descarte, (motivo, localDescarte, idEPI, quantidade_descartar))
                conexao.commit()

                comando_update_estoque = 'UPDATE epi SET quantidade = quantidade - %s WHERE idEPI = %s'
                cursor.execute(comando_update_estoque, (quantidade_descartar, idEPI))
                conexao.commit()

                # Atualiza a tabela epi_funcionário
                comando_update_epi_funcionario = '''
                    UPDATE epi_funcionário 
                    SET quantidade = quantidade - %s 
                    WHERE idEPI_Funcionario = %s
                '''
                cursor.execute(comando_update_epi_funcionario, (quantidade_descartar, id))
                conexao.commit()

                if quantidade_descartar == quantidade_atual:
                    comando_delete_epi_funcionario = 'DELETE FROM epi_funcionário WHERE idEPI_Funcionario = %s'
                    cursor.execute(comando_delete_epi_funcionario, (id,))
                    conexao.commit()

                cursor.execute('SELECT nomeEquipamento FROM epi WHERE idEPI = %s', (idEPI,))
                nomeEPI = cursor.fetchone()[0]

                comando_inserir_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Descarte de EPI: {nomeEPI}"
                cursor.execute(comando_inserir_backlog, (acao, idSupervisor))
                conexao.commit()

                return redirect('/estoque')

            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

@admin_blueprint.route('/descricaoDescarte/<int:idEPI>', methods=['POST'])
def excluirDescarte(idEPI):
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT * FROM descarte WHERE idEquipamento = %s', (idEPI,))
            descarte = cursor.fetchone()

            if not descarte:
                return "Descarte não encontrado", 404

          
            cursor.execute('DELETE FROM descarte WHERE idEquipamento = %s', (idEPI,))
            conexao.commit()

           
            cursor.execute('DELETE FROM epi WHERE idEPI = %s', (idEPI,))
            conexao.commit()

          
            idSupervisor = 1  
            comando_backlog = '''
                INSERT INTO Backlog (dataHora, acao, idSupervisor)
                VALUES (NOW(), %s, %s)
            '''
            acao = f"Exclusão do descarte e do EPI: {idEPI}"
            cursor.execute(comando_backlog, (acao, idSupervisor))
            conexao.commit()

            return redirect('/descarte') 
    except Exception as e:
        return f"Erro ao excluir o descarte e o EPI: {e}", 500, 

