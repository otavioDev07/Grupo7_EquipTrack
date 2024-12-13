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

