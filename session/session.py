from flask import session, redirect, url_for, flash
from functools import wraps

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'idSupervisor' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login.login'))
        return func(*args, **kwargs)
    return wrapper

# from werkzeug.security import generate_password_hash, check_password_hash

# def gerar_hash(senha_plana):
#     return generate_password_hash(senha_plana)

# def verificar_senha(senha_plana, senha_hash):
#     return check_password_hash(senha_hash, senha_plana)

# senha_plana = "senha"
# senha_hash = gerar_hash(senha_plana)

# print(f"Hash gerado: {senha_hash}")

# senha = input('Senha: ')
# if verificar_senha(senha, senha_hash):
#     print("Senha correta!")
# else:
#     print("Senha incorreta!")
