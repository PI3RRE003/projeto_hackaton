from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, socketio
from app.controllers import auth_controller, paciente_controller, profissional_controller, chat_controller
import click
from flask.cli import with_appcontext

def create_app():
    app = Flask(__name__)  
    app.config.from_object(Config)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_api'
    socketio.init_app(app, async_mode=app.config['SOCKETIO_ASYNC_MODE'])
    
    # Registrar blueprints
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(paciente_controller.bp)
    app.register_blueprint(profissional_controller.bp)
    app.register_blueprint(chat_controller.bp)  # NOVO: Blueprint do chat
    
    app.cli.add_command(init_db_command)

    return app

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Limpa os dados existentes e cria novas tabelas."""
    db.drop_all()
    db.create_all()
    click.echo('Banco de dados inicializado!')