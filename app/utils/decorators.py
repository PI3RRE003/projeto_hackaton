from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def paciente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username!= 'paciente':
            flash('Acesso restrito a pacientes.', 'warning')
            return redirect(url_for('auth.login_api'))
        return f(*args, **kwargs)
    return decorated_function

def profissional_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username != 'profissional':
            flash('Acesso restrito a profissionais.', 'warning')
            return redirect(url_for('auth.login_api'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'admin':
            flash('Acesso restrito a administradores.', 'warning')
            return redirect(url_for('auth.login_api'))
        return f(*args, **kwargs)
    return decorated_function