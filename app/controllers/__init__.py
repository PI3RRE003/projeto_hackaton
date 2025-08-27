from app.controllers.auth_controller import bp as auth_bp
from app.controllers.chat_controller import bp as chat_bp
from app.controllers.paciente_controller import bp as paciente_bp
from app.controllers.profissional_controller import bp as profissional_bp

__all__ = ['auth_bp', 'chat_bp', 'paciente_bp', 'profissional_bp']