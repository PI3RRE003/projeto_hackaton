from app.extensions import db
from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
class Registro:
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    registro = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    paciente = db.relationship('Paciente', backref=db.backref('registros_manha', lazy=True))
    profissional = db.relationship('Profissional', backref=db.backref('registros_manha', lazy=True))

    @classmethod
    def get_registro_hoje(cls, paciente_id):
        hoje = date.today()
        return cls.query.filter_by(paciente_id=paciente_id, data=hoje).first()
    
    @classmethod
    def get_registros_por_paciente(cls, paciente_id):
        return cls.query.filter_by(paciente_id=paciente_id).order_by(cls.data.desc()).all()
    
    @classmethod
    def get_all_registros(cls):
        return cls.query.order_by(cls.data.desc()).all()