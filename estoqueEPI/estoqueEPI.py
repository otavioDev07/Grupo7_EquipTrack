from flask import render_template, Blueprint, request
from session.session import require_login
from database.conection import conecta_db
from datetime import datetime, timedelta

estoque_blueprint = Blueprint('estoqueEPI', __name__, template_folder="templates")

@estoque_blueprint.route('/estoque', methods=['GET'])
@require_login
def get_estoque():
    filtro = request.args.get('filtro', 'no_prazo')  # Filtro padrão: 'no_prazo'

    query_base = '''
        SELECT idEPI, codigoCA, nomeEquipamento, quantidade, dataVencimento 
        FROM epi 
        WHERE status != "Descartado"
    '''
    filtros = {
        'no_prazo': 'AND dataVencimento > CURDATE() + INTERVAL 30 DAY',
        'perto_vencimento': 'AND dataVencimento BETWEEN CURDATE() AND CURDATE() + INTERVAL 30 DAY',
        'vencido': 'AND dataVencimento < CURDATE()'
    }
    filtro_query = filtros.get(filtro, '')

    try:
        with conecta_db() as (conexao, cursor):

            comando_update = 'UPDATE epi SET status = "Descartado" WHERE quantidade = 0 AND status != "Descartado"'
            cursor.execute(comando_update)
            conexao.commit()
            
            query_final = f"{query_base} {filtro_query}"
            cursor.execute(query_final)
            EPIs = cursor.fetchall()

            return render_template('estoqueEPI.html', EPIs=EPIs, filtro=filtro)
    except Exception as e:
        print("Erro ao buscar dados:", e)
        return "Erro ao buscar dados", 500

@estoque_blueprint.route('/buscaEPI', methods=['POST'])
def buscaEPI():
    pesquisa = request.form.get('pesquisa')
    if not pesquisa:
        return "Campo de pesquisa está vazio", 400

    with conecta_db() as (conexao, cursor):
        query = '''
            SELECT idEPI, codigoCA, nomeEquipamento, quantidade, dataVencimento FROM EPI WHERE nomeEquipamento LIKE CONCAT('%', %s, '%')
        '''
        cursor.execute(query, (pesquisa,))
        EPIs = cursor.fetchall()

        #Verificação do status
        if EPIs[4] > datetime.now() + timedelta(days=30):
            filtro = 'no_prazo'
        elif EPIs[4] <= datetime.now() + timedelta(days=30):
            filtro = 'perto_vencimento'
        else:
            status = 'vencido'
        return render_template('estoqueEPI.html', EPIs=EPIs, filtro=filtro)
    
        