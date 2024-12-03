from flask import render_template, Blueprint, request, redirect, session
from database.conection import *
from datetime import datetime
from datetime import date
from mysql.connector import Error
from session.session import require_login

admin_blueprint = Blueprint('admin', __name__, template_folder="templates")

@admin_blueprint.route('/cadastroEPI', methods=['GET','POST'])
@require_login
def cadastro_EPI():
    if request.method == 'GET':
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT * FROM setor')
            setores = cursor.fetchall()
            return render_template('cadastroEPI.html',setores=setores)
    
    if request.method == 'POST':
        with conecta_db() as (conexao, cursor):
            try:
                codigoCA = request.form['ca']
                numeroSerie = request.form['numero-serie']
                marca = request.form['marca']
                nomeEquipamento = request.form['nome']
                dataAquisicao = request.form['dataAquisicao']
                quantidade = request.form['quantidade']
                dataVencimento = request.form['dataVencimento']

                idSetor = request.form['idSetor'] #Verificar se o valor está vindo 
                idSupervisor = session['idSupervisor']

                modelo = request.form.get('modelo')
                observacoes = request.form.get('observacoes')
                tamanho = request.form.get('tamanho')

                
                status = 'Estoque'

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
                return redirect('/home')
            except Exception as e:
                return f"Erro de BackEnd: {e}"
            except Error as e:
                return f"Erro de BD:{e}"

@admin_blueprint.route('/editarEPI/<int:idEPI>', methods=['GET', 'POST'])
@require_login
def editarEPI(idEPI):
    with conecta_db() as (conexao, cursor):
        if request.method == 'GET':
            try:
                cursor.execute('SELECT nomeEquipamento, numeroSerie, codigoCA, marca, modelo, dataAquisicao, dataVencimento, idSetor, status, quantidade, observacoes, tamanho FROM epi WHERE idEPI = %s', (idEPI,))
                epi = cursor.fetchone()
                if epi:
                    cursor.execute('SELECT idSetor, nomeSetor FROM setor')
                    setores = cursor.fetchall()

                    return render_template('edicaoEPI.html', epi=epi, setores=setores, idEPI=idEPI)
                else:
                    return "EPI não encontrado", 404
            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

        if request.method == 'POST':
            try:
                nome = request.form['nome']
                numero_serie = request.form['numero-serie']
                ca = request.form['ca']
                marca = request.form['marca']
                modelo = request.form.get('modelo', '') 
                data_aquisicao = request.form['dataAquisicao']
                data_vencimento = request.form['dataVencimento']
                setor_id = request.form['setor']
                quantidade = request.form['quantidade']
                observacoes = request.form.get('observacoes', '')  
                tamanho = request.form.get('tamanho', '') 

                comando = '''
                    UPDATE epi
                    SET nomeEquipamento = %s, numeroSerie = %s, codigoCA = %s, marca = %s, modelo = %s,
                        dataAquisicao = %s, dataVencimento = %s, idSetor = %s, quantidade = %s, observacoes = %s, tamanho = %s
                    WHERE idEPI = %s
                '''
                cursor.execute(comando, (nome, numero_serie, ca, marca, modelo, data_aquisicao,
                                         data_vencimento, setor_id, quantidade, observacoes,
                                         tamanho, idEPI))
                conexao.commit()

                idSupervisor = session['idSupervisor']
                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                acao = f"Edição de EPI: {nome}" 
                cursor.execute(comando_backlog, (acao, idSupervisor))   
                conexao.commit()

                return redirect(f'/descricaoEPI/{idEPI}') 
            except Exception as e:
                return f"Erro ao salvar as edições: {e}", 500


@admin_blueprint.route('/cadastroFuncionario', methods=['GET','POST'])
@require_login
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
                idSupervisor = session['idSupervisor']
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
                return redirect('/home')

            except Exception as e:
                return f"Erro de BackEnd: {e}"
            except Error as e:
                return f"Erro de BD:{e}"
                

@admin_blueprint.route('/descarte')
@require_login
def descarte():
    query = '''
        SELECT e.idEPI, e.codigoCA, e.nomeEquipamento, d.quantidade, d.idDescarte
        FROM epi e
        INNER JOIN descarte d ON d.idEquipamento = e.idEPI
    '''
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute(query)
            EPIs = cursor.fetchall()
            return render_template('descarte.html', EPIs=EPIs)
    except Exception as e:
        print("Erro ao buscar dados:", e)
        return "Erro ao buscar dados", 500
    
@admin_blueprint.route('/descricaoDescarte/<int:idDescarte>', methods=['GET'])
@require_login
def descricaoDescarte(idDescarte):
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute('''
                SELECT d.idEquipamento, d.motivoDescarte, d.localDescarte, d.dataDescarte, d.quantidade, 
                       e.codigoCA, e.numeroSerie, e.marca, e.modelo, e.dataVencimento, e.status, 
                       e.observacoes, e.nomeEquipamento, e.dataAquisicao, e.tamanho, e.quantidade, 
                       s.nomeSetor
                FROM descarte d
                JOIN epi e ON d.idEquipamento = e.idEPI
                JOIN setor s ON e.idSetor = s.idSetor
                WHERE d.idDescarte = %s
            ''', (idDescarte,))
            
            result = cursor.fetchone()
            
            if result:
                epi = {
                    'idEPI': result[0],
                    'codigoCA': result[5],
                    'numeroSerie': result[6],
                    'marca': result[7],
                    'modelo': result[8],
                    'dataVencimento': result[9],
                    'status': result[10],
                    'observacoes': result[11],
                    'nomeEquipamento': result[12],
                    'dataAquisicao': result[13],
                    'tamanho': result[14],
                    'quantidade': result[15],
                    'nomeSetor': result[16]
                }
                
                descarte = {
                    'idDescarte': idDescarte,
                    'motivoDescarte': result[1],
                    'localDescarte': result[2],
                    'dataDescarte': result[3],
                    'quantidade': result[4]
                }

                return render_template('descricaoDescarte.html', epi=epi, descarte=descarte)
            else:
                return "Descarte não encontrado.", 404

    except Exception as e:
        return f"Ocorreu um erro: {e}", 500
        
@admin_blueprint.route('/cadastroDescarte/<int:idEPI>', methods=['GET', 'POST'])
@require_login
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
                idSupervisor = session['idSupervisor'] 

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
                return redirect('/estoque')

            except Exception as e:
                return f"Erro de BackEnd: {e}", 500
            

@admin_blueprint.route('/editDescarte/<int:idDescarte>', methods=['GET', 'POST'])
@require_login
def editDescarte(idDescarte):
    with conecta_db() as (conexao, cursor):
        if request.method == 'GET':
            try:
                cursor.execute('''
                    SELECT d.idDescarte, d.motivoDescarte, d.localDescarte, d.quantidade, e.nomeEquipamento, e.idEPI
                    FROM descarte d
                    INNER JOIN epi e ON d.idEquipamento = e.idEPI
                    WHERE d.idDescarte = %s
                ''', (idDescarte,))
                result = cursor.fetchone()

                if result:
                    descarte = {
                        'idDescarte': result[0],
                        'motivoDescarte': result[1],
                        'localDescarte': result[2],
                        'quantidade': int(result[3]),
                        'nomeEquipamento': result[4],
                        'idEPI': result[5]
                    }
                else:
                    return "Erro: Descarte não encontrado.", 404
                
                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (descarte['idEPI'],))
                result = cursor.fetchone()
                if result:
                    quantidadeDisponivel = result[0]
                else:
                    return "Erro: EPI não encontrado.", 404
                
                return render_template(
                    'edicaoDescarte.html', 
                    descarte=descarte, 
                    quantidadeDisponivel=quantidadeDisponivel
                )
            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

        elif request.method == 'POST':
            try:
                novo_motivo = request.form['motivoDescarte']
                novo_localDescarte = request.form['localDescarte']
                nova_quantidade = int(request.form['quantidade'])

                cursor.execute('SELECT idEquipamento FROM descarte WHERE idDescarte = %s', (idDescarte,))
                result = cursor.fetchone()
                if result:
                    idEPI = result[0]
                else:
                    return "Erro: Registro de descarte não encontrado.", 404

                cursor.execute('SELECT quantidade FROM epi WHERE idEPI = %s', (idEPI,))
                result = cursor.fetchone()
                if result:
                    quantidade_atual = result[0]
                else:
                    return "Erro: EPI não encontrado.", 404
                
                cursor.execute('SELECT quantidade FROM descarte WHERE idDescarte = %s', (idDescarte,))
                result = cursor.fetchone()
                if result:
                    quantidade_descartada_anterior = result[0]
                else:
                    return "Erro: Registro de descarte não encontrado.", 404
                
                ajuste_quantidade = nova_quantidade - quantidade_descartada_anterior
                if ajuste_quantidade > quantidade_atual:
                    return "Erro: A quantidade ajustada excede o estoque disponível.", 400
                
                cursor.execute('UPDATE epi SET quantidade = quantidade - %s WHERE idEPI = %s', 
                               (ajuste_quantidade, idEPI))
                conexao.commit()

                cursor.execute('''
                    UPDATE descarte 
                    SET motivoDescarte = %s, localDescarte = %s, quantidade = %s, dataDescarte = NOW() 
                    WHERE idDescarte = %s
                ''', (novo_motivo, novo_localDescarte, nova_quantidade, idDescarte))
                conexao.commit()

                comando_backlog = '''
                    INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                    VALUES (NOW(), %s, %s)
                '''
                idSupervisor = session['idSupervisor']  
                acao = f"Edição de descarte do EPI: {idEPI}"
                cursor.execute(comando_backlog, (acao, idSupervisor))
                conexao.commit()

                return redirect(f'/descricaoDescarte/{idDescarte}')

            except Exception as e:
                return f"Erro de BackEnd: {e}", 500
            
@admin_blueprint.route('/editarFuncionario/<int:idFuncionario>', methods=['GET', 'POST'])
@require_login
def editarFuncionario(idFuncionario):
    with conecta_db() as (conexao, cursor):
        if request.method == 'GET':
            try:
                query = '''
                    SELECT nomeFuncionário, CPF, NIF, cargo, idSetor, tamRoupa, tamCalcado, condicoesEspeciais
                    FROM funcionário
                    WHERE idFuncionario = %s
                '''
                cursor.execute(query, (idFuncionario,))
                result = cursor.fetchone()

                if result:
                    funcionario = {
                        'nome': result[0],
                        'CPF': result[1],
                        'nif': result[2],
                        'cargo': result[3],
                        'idSetor': result[4],
                        'tamanhoRoupa': result[5],
                        'calcados': result[6],
                        'condicoesEspeciais': result[7],
                    }
                    cursor.execute('SELECT idSetor, nomeSetor FROM setor')
                    setores = cursor.fetchall()

                    return render_template('edicaoFuncionario.html', funcionario=funcionario, setores=setores, idFuncionario=idFuncionario)
                else:
                    return "Funcionário não encontrado", 404
            except Exception as e:
                return f"Erro de BackEnd: {e}", 500

        if request.method == 'POST':
                try:
                    nome = request.form['nome']
                    cpf = request.form['cpf']
                    nif = request.form['nif']
                    cargo = request.form['cargo']
                    idSetor = request.form['idSetor']
                    tamanhoRoupa = request.form['tamanhoRoupa']
                    calcados = request.form['calcados']
                    condicoesEspeciais = request.form['condicoesEspeciais']

                    query = '''
                        UPDATE funcionário
                        SET nomeFuncionário = %s, CPF = %s, NIF = %s, cargo = %s, idSetor = %s, 
                            tamRoupa = %s, tamCalcado = %s, condicoesEspeciais = %s
                        WHERE idFuncionario = %s
                    '''
                    cursor.execute(query, (nome, cpf, nif, cargo, idSetor, tamanhoRoupa, calcados, condicoesEspeciais, idFuncionario))
                    conexao.commit()

                    idSupervisor = session['idSupervisor']
                    comando_inserir_backlog = '''
                        INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                        VALUES (NOW(), %s, %s)
                    '''
                    acao = f"Edição do Funcionário: {nome}"
                    cursor.execute(comando_inserir_backlog, (acao, idSupervisor))
                    conexao.commit()

                    return redirect(f'/descFuncionario/{idFuncionario}')
                except Exception as e:
                    return f"Erro ao salvar as edições: {e}", 500

@admin_blueprint.route('/descricaoEPI/<int:idEPI>', methods=['GET'])
@require_login
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
                    'dataVencimento': result[5],
                    'status': result[6],
                    'observacoes': result[7],
                    'nomeEquipamento': result[8],
                    'dataAquisicao': result[9],
                    'tamanho': result[10],
                    'quantidade': result[11],
                    'nomeSetor': nomeSetor
                }
                return render_template('descricaoEPI.html', epi=epi)
            else:
                return "EPI não encontrado", 404

        except Exception as e:
            return f"Erro de BackEnd: {e}"
            
        
@admin_blueprint.route('/funcionarios/<int:idSetor>', methods=['GET'])
@require_login
def get_funcionarios(idSetor):
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT idFuncionario, nomeFuncionário, NIF, cargo FROM funcionário WHERE idSetor = %s', (idSetor,))
            funcionarios = cursor.fetchall() 

            cursor.execute('SELECT nomeSetor FROM setor WHERE idSetor = %s', (idSetor,))
            nomeSetor = cursor.fetchone() 

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
@require_login
def descFuncionario(idFuncionario):
    try:
        with conecta_db() as (conexao, cursor):
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
@require_login
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
@require_login
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
                idSupervisor = session['idSupervisor']  

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

@admin_blueprint.route('/excluirDescarte/<int:idDescarte>', methods=['POST'])
@require_login
def excluirDescarte(idDescarte):
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute('SELECT idEquipamento FROM descarte WHERE idDescarte = %s', (idDescarte,))
            result = cursor.fetchone()

            if not result:
                return "Descarte não encontrado", 404

            idEPI = result[0]  

            cursor.execute('DELETE FROM descarte WHERE idDescarte = %s', (idDescarte,))
            conexao.commit()

            idSupervisor = session['idSupervisor']  
            comando_backlog = '''
                INSERT INTO Backlog (dataHora, acao, idSupervisor)
                VALUES (NOW(), %s, %s)
            '''
            acao = f"Exclusão do descarte do EPI: {idEPI}"
            cursor.execute(comando_backlog, (acao, idSupervisor))
            conexao.commit()

            return redirect('/descarte') 

    except Exception as e:
        return f"Erro ao excluir o descarte e o EPI: {e}", 500

