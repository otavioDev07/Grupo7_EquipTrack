from flask import Blueprint
import mysql.connector
from contextlib import contextmanager

db_blueprint = Blueprint('database', __name__)

DB_CONFIG = {
    'host': '10.142.227.160',
    'user': 'root',
    'password': 'senai',
    'database': 'equiptrack'
}


@contextmanager
def conecta_db():
    conexaoDB = mysql.connector.connect(**DB_CONFIG)
    cursorDB = conexaoDB.cursor()
    try:
        yield conexaoDB, cursorDB  # "empresta" a conexão e o cursor para o bloco "with"
    finally:
        cursorDB.close()  # Garante que o cursor será fechado
        conexaoDB.close()  # Garante que a conexão será fechada