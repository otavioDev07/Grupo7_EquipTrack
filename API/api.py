from flask import Flask, jsonify, request
from flask_cors import CORS
from database.conection import conecta_db

app = Flask(__name__)
CORS(app)

#Listagem do estoque
@app.route('/listEPI', methods=['GET'])
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
        
#Listagem dos funcionários
@app.route('/listFuncionarios/<id>', methods=['GET'])
def list_funcionarios(id):
    with conecta_db() as (conexao, cursor):
        try:
            cursor.execute(f'SELECT idFuncionario, nomeFuncionário, NIF, cargo FROM funcionário WHERE idSetor = {id}')
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

if __name__ == '__main__':
    app.run(debug=True)