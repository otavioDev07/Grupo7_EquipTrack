from flask import render_template, Blueprint
from database.conection import conecta_db

home_blueprint = Blueprint('home', __name__, template_folder="templates")

@home_blueprint.route('/')
@home_blueprint.route('/home', methods=['GET'])
def home():
    with conecta_db() as (conexao, cursor):
        cursor.execute('SELECT * FROM backlog')
        backlog = cursor.fetchall()
    return render_template('home.html', backlog=backlog)