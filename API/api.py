from flask import Flask, jsonify, request, Blueprint
from datetime import datetime
from database.conection import conecta_db
from datetime import datetime

api_blueprint = Blueprint('API', __name__)

#Listagem de EPIs
@api_blueprint.route('/listEPI', methods=['GET'])
def list_EPI():
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute('SELECT idEPI, codigoCA, nomeEquipamento, quantidade, status FROM epi')
            result = cursor.fetchall()
            
            estoque = []
            for row in result:
                estoque.append({
                    'idEPI': row[0],
                    'codigoCA': row[1],
                    'nomeEquipamento': row[2],
                    'quantidade': row [3],
                    'status': row[4]
                })

            return jsonify(estoque), 200 
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
#EPI específico
@api_blueprint.route('/EPI/<id>', methods=['GET'])
def get_EPI(id):
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute(f'SELECT * FROM epi WHERE idEPI = {id}')
            result = cursor.fetchone()

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
            'idSetor': result[13],
            }

            return jsonify(epi), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
#Listagem dos funcionários
@api_blueprint.route('/listFuncionarios/<idSetor>', methods=['GET'])
def list_funcionarios(idSetor):
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute(f'SELECT idFuncionario, nomeFuncionário, NIF, cargo FROM funcionário WHERE idSetor = {idSetor}')
            result = cursor.fetchall()

            funcionarios = []
            for row in result:
                funcionarios.append({
                    'idFuncionario': row[0],
                    'nomeFuncionário': row[1],
                    'NIF': row[2],
                    'cargo': row[3],
                })
            return jsonify(funcionarios), 200 
        except Exception as e:
            return jsonify({'error': str(e)}), 400 
        
#Listagem do Backlog
@api_blueprint.route('/listBacklog', methods=['GET'])
def list_backlog():
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute('SELECT * FROM backlog')
            result = cursor.fetchall()

            backlog = []

            for row in result:
                backlog.append({
                    'idBacklog': row[0],
                    'dataHora': row[1],
                    'acao': row[2],
                    'idSupervisor': row[3]
                })
            return jsonify(backlog), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400 
        
#Cadastro de EPI
@api_blueprint.route('/cadEPI', methods=['POST'])
def cad_EPI():
    data = request.json
    with conecta_db() as (conexao, cursor):
        try:
            # Campos obrigatórios
            codigoCA = data['codigoCA']
            numeroSerie = data['numeroSerie']
            marca = data['marca']
            nomeEquipamento = data['nomeEquipamento']
            dataAquisicao = data['dataAquisicao']
            quantidade = data['quantidade']
            dataVencimento = data['dataVencimento']
            idSetor = data['idSetor'] 
            idSupervisor = data['idSupervisor']


            # Campos opcionais
            modelo = data.get('modelo')
            dataLocacao = data.get('dataLocacao')
            observacoes = data.get('observacoes')
            tamanho = data.get('tamanho')

            # Validação do campo `status`
            status = data['status']
            if status not in ["Em uso", "Estoque"]:
                return jsonify({'error': 'Status inválido. Deve ser "Em uso" ou "Estoque".'}), 400

            # Validação das datas
            try:
                dataVencimento = datetime.strptime(dataVencimento, '%Y-%m-%d').date()
                dataAquisicao = datetime.strptime(dataAquisicao, '%Y-%m-%d %H:%M:%S')
                if dataLocacao:
                    dataLocacao = datetime.strptime(dataLocacao, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use o formato AAAA-MM-DD.'}), 400

            comando = '''
                INSERT INTO EPI (codigoCA, numeroSerie, marca, modelo, dataLocacao, dataVencimento, status, observacoes, nomeEquipamento, dataAquisicao, tamanho, quantidade, idSetor) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(comando, (codigoCA, numeroSerie, marca, modelo, dataLocacao, dataVencimento, status, observacoes, nomeEquipamento, dataAquisicao, tamanho, quantidade, idSetor))
            conexao.commit()

            # Retornar o ID gerado
            last_id = cursor.lastrowid
            comando_backlog = '''
                INSERT INTO Backlog (dataHora, acao, idSupervisor) 
                VALUES (NOW(), %s, %s)
            '''
            acao = f"Cadastro de EPI: {nomeEquipamento}" 
            cursor.execute(comando_backlog, (acao, idSupervisor))   
            conexao.commit()
            return jsonify({'message': 'Sucesso!', 'idEPI': last_id}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400 
        




#ERRO 404
@api_blueprint.errorhandler(404)
def pagina_nao_encontrada(erro):
    return jsonify({'erro':'Página não encontrada!'}),404

#ERRO 405
@api_blueprint.errorhandler(405)
def metodo_invalido(erro):
    return jsonify({'erro':'Método HTTP inválido'}), 405

#ERRO 500
@api_blueprint.errorhandler(500)
def erro_servidor(erro):
    return jsonify({'erro':'Erro interno no servidor'}), 500

if __name__ == '__main__':
    api_blueprint.run(debug=True)