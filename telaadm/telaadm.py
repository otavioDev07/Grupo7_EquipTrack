from flask import render_template, Blueprint

telaadm_blueprint = Blueprint('telaadm', __name__, template_folder="templates")

@telaadm_blueprint.route('/telaadm')
def telaadm():
    return render_template('telaadm.html', titulo_pagina="Gerenciamento")

@telaadm_blueprint.route('/vercipeiros')
def vercipeiros():
    return render_template('vercipeiros.html', titulo_pagina="Cipeiros")