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
            cursor.execute('SELECT * FROM EPI')
            result = cursor.fetchall()
            
            estoque = []
            for row in result:
                estoque.append({
                    'idEPI': row[0],
                    'numSerieEPI': row[1],
                    'marca': row[2],
                    'modelo': row[3],
                    'dataLocacao': row[4],
                    'dataVencimento': row[5],
                    'status': row[6],
                    'observacoes': row[7],
                    'nomeEquipamento': row[8],
                    'dataAquisicao': row[9],
                    'tamanho': row[10],
                    'idSetor': row[11],
                    'idCategoria': row[12],
                    'quantidade': row[13]
                })

            return jsonify(estoque), 200 
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)