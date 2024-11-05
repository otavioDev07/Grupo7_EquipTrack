from flask import render_template, Blueprint
from database.conection import conecta_db

estoque_blueprint = Blueprint('estoqueEPI', __name__, template_folder="templates")

@estoque_blueprint.route('/estoque', methods=['GET'])
def get_estoque():
    try:
        with conecta_db as (conexao, cursor):
            EPIs = cursor.execute('SELECT (idEPI, codigoCA, nomeEquipamento, quantidade) FROM epi WHERE  ')
    except: 
        ...