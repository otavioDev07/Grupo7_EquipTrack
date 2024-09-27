from flask import Blueprint
import mysql.connector

database_blueprint = Blueprint('database', __name__)

def conexao_DB():
    conexaoDB = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "senai",
    database = "equiptrack"
    )
    return conexaoDB