from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_manager
from app.models import Profissional, Paciente
from app.extensions import db, login_manager

bp = Blueprint('auth', __name__)


@login_manager.user_loader

def load_user(user_id):
    # Tenta buscar primeiro profissional
    user = Profissional.query.get(user_id)
    if not user:
    # Se não achar, tenta paciente
        user = Paciente.query.get(user_id)
    return user

@bp.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username e password são obrigatórios"}), 400

    # Primeiro profissional, depois paciente
    user = Profissional.query.filter_by(username=username).first()
    if not user:
        user = Paciente.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        tipo = "profissional" if isinstance(user, Profissional) else "paciente"
        return jsonify({"success": True,"message":"Login realizado com sucesso", "user_id": user.id, "tipo": tipo}), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401