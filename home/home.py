from flask import render_template, Blueprint
from session.session import require_login
from database.conection import conecta_db

home_blueprint = Blueprint('home', __name__, template_folder="templates")

@home_blueprint.route('/home', methods=['GET'])
@require_login
def home():
    with conecta_db() as (conexao, cursor):
        try:
            comando_update = '''
                UPDATE epi 
                SET status = "Descartado" 
                WHERE quantidade = 0 AND status != "Descartado"
            '''
            cursor.execute(comando_update)
            conexao.commit()

            comando_setores = '''
                SELECT s.idSetor, s.nomeSetor
                FROM setor s
            '''
            cursor.execute(comando_setores)
            setores = cursor.fetchall() 

            # Contar EPIs vencidos e próximos do vencimento para cada setor
            setores_data = []
            for setor in setores:
                idSetor = setor[0]
                
                # Verificar os EPIs associados aos funcionários desse setor
                comando_epi = '''
                    SELECT 
                        SUM(CASE WHEN e.dataVencimento < CURDATE() THEN 1 ELSE 0 END) AS vencidos,
                        SUM(CASE WHEN e.dataVencimento BETWEEN CURDATE() AND CURDATE() + INTERVAL 30 DAY THEN 1 ELSE 0 END) AS perto_vencimento
                    FROM epi e
                    JOIN funcionário f ON e.idFuncionario = f.idFuncionario
                    WHERE f.idSetor = %s
                '''
                cursor.execute(comando_epi, (idSetor,))
                epi_data = cursor.fetchone()

                # Se não houver EPIs ou funcionários, marcar como 0
                vencidos = epi_data[0] if epi_data[0] else 0
                perto_vencimento = epi_data[1] if epi_data[1] else 0

                setores_data.append({
                    'idSetor': idSetor,
                    'nomeSetor': setor[1],
                    'vencidos': vencidos,
                    'perto_vencimento': perto_vencimento
                })

        except Exception as e:
            return f"Erro de BackEnd: {e}", 500

    return render_template('home.html', setores=setores_data)