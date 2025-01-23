from flask import Blueprint
import mysql.connector
from contextlib import contextmanager

db_blueprint = Blueprint('database', __name__)

#Preencha com seu banco de dados
DB_CONFIG = {
    'host': '',
    'user': '',
    'password': '',
    'database': 'equiptrack'
}

@contextmanager
def conecta_db():
    conexaoDB = mysql.connector.connect(**DB_CONFIG)
    cursorDB = conexaoDB.cursor(buffered=True)
    try:
        yield conexaoDB, cursorDB  # "empresta" a conexão e o cursor para o bloco "with"
    finally:
        cursorDB.close()  # Garante que o cursor será fechado
        conexaoDB.close()  # Garante que a conexão será fechada