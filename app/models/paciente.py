from app.extensions import db
from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from app.models.associations import profissional_paciente

class Paciente(db.Model,UserMixin):#tudo que tem no model e mixin
    #colunas id(int), username(text), password(text)
    __tablename__ = "paciente"
    id = db.Column(db.Integer, primary_key=True) #chave primaria = unica
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com as mensagens
    mensagens = db.relationship(
    'MensagemChat',
    back_populates='paciente',
    lazy=True,
    cascade="all, delete-orphan"
    )

    profissionais = db.relationship(
        'Profissional',
        secondary=profissional_paciente,
        back_populates="pacientes"
    )

    from app.extensions import db

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Paciente {self.username}>'