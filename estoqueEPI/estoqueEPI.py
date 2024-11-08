from flask import render_template, Blueprint, request
from database.conection import conecta_db

estoque_blueprint = Blueprint('estoqueEPI', __name__, template_folder="templates")

@estoque_blueprint.route('/estoque', methods=['GET'])
def get_estoque():
    filtro = request.args.get('filtro', 'no_prazo')  # 'no_prazo' como padrão
    query = 'SELECT idEPI, codigoCA, nomeEquipamento, quantidade FROM epi'
    
    if filtro == 'no_prazo':
        query += ' WHERE dataVencimento > CURDATE() + INTERVAL 30 DAY' 
    elif filtro == 'perto_vencimento':
        query += ' WHERE dataVencimento BETWEEN CURDATE() AND CURDATE() + INTERVAL 30 DAY'
    elif filtro == 'vencido':
        query += ' WHERE dataVencimento < CURDATE()'
    
    try:
        with conecta_db() as (conexao, cursor):
            cursor.execute(query)
            EPIs = cursor.fetchall()
            return render_template('estoqueEPI.html', EPIs=EPIs, filtro=filtro)
    except Exception as e:
        print("Erro ao buscar dados:", e)
        return "Erro ao buscar dados", 500
        