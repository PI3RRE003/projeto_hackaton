from app.extensions import db

profissional_paciente = db.Table(
    'profissional_paciente',
    db.Column('profissional_id', db.Integer, db.ForeignKey('profissional.id'), primary_key=True),
    db.Column('paciente_id', db.Integer, db.ForeignKey('paciente.id'), primary_key=True)
)
