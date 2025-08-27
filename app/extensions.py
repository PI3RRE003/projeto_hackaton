from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask import jsonify


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = None  # desativa redirect
login_manager.login_message = None

@login_manager.unauthorized_handler
def unauthorized_callback():
    return jsonify({"error": "Não autorizado"}), 401
socketio = SocketIO()