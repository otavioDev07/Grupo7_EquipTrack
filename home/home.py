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

            # Obtém os setores
            comando_setores = '''
                SELECT s.idSetor, s.nomeSetor
                FROM setor s
            '''
            cursor.execute(comando_setores)
            setores = cursor.fetchall()

            setores_data = []
            for setor in setores:
                idSetor = setor[0]
                comando_epi_funcionario = '''
                SELECT 
                    SUM(CASE 
                        WHEN e.dataVencimento < CURDATE() THEN 1 
                        ELSE 0 
                    END) AS vencidos,
                    SUM(CASE 
                        WHEN e.dataVencimento BETWEEN CURDATE() AND CURDATE() + INTERVAL 30 DAY THEN 1 
                        ELSE 0 
                    END) AS perto_vencimento
                FROM epi_funcionário ef
                JOIN epi e ON ef.idEquipamento = e.idEPI
                JOIN funcionário f ON ef.idFuncionario = f.idFuncionario
                WHERE f.idSetor = %s AND e.status != "Descartado"
                '''
                cursor.execute(comando_epi_funcionario, (idSetor,))
                epi_data = cursor.fetchone()

                vencidos = epi_data[0] if epi_data[0] else 0
                perto_vencimento = epi_data[1] if epi_data[1] else 0

                setores_data.append({
                    'idSetor': idSetor,
                    'nomeSetor': setor[1],
                    'vencidos': vencidos,
                    'perto_vencimento': perto_vencimento
                })

            return render_template('home.html', setores=setores_data)

        except Exception as e:
            return f"Erro de BackEnd: {e}", 500

    return render_template('home.html', setores=setores_data)