from app.extensions import db
from app.models import Paciente

class PacienteRepository:
    @staticmethod
    def obter_por_id(paciente_id):
        return Paciente.query.get(paciente_id)
    
    @staticmethod
    def obter_por_user_id(user_id):
        return Paciente.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def obter_todos():
        return Paciente.query.all()
    
    @staticmethod
    def criar(paciente_data):
        paciente = Paciente(**paciente_data)
        db.session.add(paciente)
        db.session.commit()
        return paciente
    
    @staticmethod
    def atualizar(paciente_id, paciente_data):
        paciente = Paciente.query.get(paciente_id)
        if paciente:
            for key, value in paciente_data.items():
                setattr(paciente, key, value)
            db.session.commit()
        return paciente