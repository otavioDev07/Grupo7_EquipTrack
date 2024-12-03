from flask import render_template, Blueprint, request
from session.session import require_login
from database.conection import conecta_db

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
    
def estoque():
    busca = request.args.get('busca', '').lower()
    filtro = request.args.get('filtro', None)

    # Simulando dados para exemplificar
    EPIs = [
        (1, '12345', 'Capacete de Segurança', 10),
        (2, '54321', 'Luva de Proteção', 5),
        # Adicione outros dados aqui
    ]

    # Filtro de busca
    if busca:
        EPIs = [item for item in EPIs if busca in item[2].lower()]
    
    # Filtro de status
    if filtro:
        if filtro == 'no_prazo':
            # Lógica para itens no prazo
            pass
        elif filtro == 'perto_vencimento':
            # Lógica para itens perto do vencimento
            pass
        elif filtro == 'vencido':
            # Lógica para itens vencidos
            pass
    
    return render_template('estoque.html', EPIs=EPIs, busca=busca, filtro=filtro)


        