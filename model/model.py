from flask import render_template, Blueprint

model_blueprint = Blueprint('model', __name__, template_folder="templates")

@model_blueprint.route('/model')
def model():
    return render_template('model.html')