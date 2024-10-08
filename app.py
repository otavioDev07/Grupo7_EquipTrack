from flask import Flask
from model.model import model_blueprint
from home.home import home_blueprint
from database.conection import db_blueprint

app = Flask(__name__)
app.secret_key = 'equipTrack'

app.register_blueprint(model_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(db_blueprint)


if __name__ == '__main__':
    app.run(debug=True)