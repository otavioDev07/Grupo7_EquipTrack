from flask import render_template, Blueprint

descarte_blueprint = Blueprint('descarte', __name__, template_folder="templates")

@descarte_blueprint.route('/descarte')
def descarte():
    return render_template('descarte.html')
