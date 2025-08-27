from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from app.models.profissional import Profissional
from app.models.paciente import Paciente

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()  # pega JSON do body
    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username e password são obrigatórios"}), 400

    # busca primeiro profissional
    user = Profissional.query.filter_by(username=username).first()
    if not user:
        user = Paciente.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        tipo = "profissional" if isinstance(user, Profissional) else "paciente"
        return jsonify({
            "message": "Login realizado com sucesso",
            "user_id": user.id,
            "tipo": tipo
        }), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout_api():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"}), 200
