from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models.associations import profissional_paciente

class Profissional(db.Model, UserMixin):
    __tablename__ = "profissional"
    id = db.Column(db.Integer, primary_key=True)  # chave primaria
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relacionamento com mensagens
    mensagens = db.relationship(
        'MensagemChat',
        back_populates='profissional',
        lazy=True,
        cascade="all, delete-orphan"
    )

    pacientes = db.relationship(
        'Paciente',
        secondary=profissional_paciente,
        back_populates="profissionais"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Profissional {self.username}>'
