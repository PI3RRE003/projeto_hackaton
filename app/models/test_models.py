# test_models.py - Arquivo temporário para testar os modelos
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos simples para teste
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Paciente {self.username}>'

class Profissional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Profissional {self.username}>'

class MensagemChat(db.Model):
    __tablename__ = 'mensagem_chat'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text)
    eh_do_paciente = db.Column(db.Boolean, default=True)
    data = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Relacionamento
    paciente = db.relationship('Paciente', backref=db.backref('mensagens', lazy=True))

if __name__ == '__main__':
    with app.app_context():
        print("Testando criação de tabelas...")
        print(f"Modelos encontrados: {list(db.metadata.tables.keys())}")
        
        # Criar tabelas
        db.drop_all()
        db.create_all()
        print("Tabelas criadas com sucesso!")
        
        # Teste de inserção
        from werkzeug.security import generate_password_hash
        
        paciente = Paciente(
            username='teste_paciente',
            password_hash=generate_password_hash('123456')
        )
        
        profissional = Profissional(
            username='teste_profissional', 
            password_hash=generate_password_hash('123456')
        )
        
        db.session.add(paciente)
        db.session.add(profissional)
        db.session.commit()
        
        # Teste de mensagem
        mensagem = MensagemChat(
            paciente_id=paciente.id,
            mensagem="Teste de mensagem",
            resposta="Teste de resposta"
        )
        
        db.session.add(mensagem)
        db.session.commit()
        
        print("Dados de teste inseridos com sucesso!")
        print(f"Pacientes: {Paciente.query.count()}")
        print(f"Profissionais: {Profissional.query.count()}")
        print(f"Mensagens: {MensagemChat.query.count()}")