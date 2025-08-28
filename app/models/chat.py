from app.extensions import db
from datetime import datetime, date

class MensagemChat(db.Model):
    __tablename__ = "mensagem_chat"
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissional.id'))
    mensagem = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text)
    eh_do_paciente = db.Column(db.Boolean, default=True)
    data = db.Column(db.Date, default=date.today, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    paciente = db.relationship('Paciente', back_populates='mensagens', lazy=True)
    profissional = db.relationship('Profissional', back_populates='mensagens', lazy=True)

    @classmethod
    def get_mensagens_hoje(cls, paciente_id):
        hoje = date.today()
        return cls.query.filter_by(paciente_id=paciente_id, data=hoje).count()
    
    @classmethod
    def pode_enviar_mensagem(cls, paciente_id):
        return cls.get_mensagens_hoje(paciente_id) < 10