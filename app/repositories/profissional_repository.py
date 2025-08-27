from app.extensions import db
from app.models import Profissional

class ProfissionalRepository:
    @staticmethod
    def obter_por_id(profissional_id):
        return Profissional.query.get(profissional_id)
    
    @staticmethod
    def obter_por_user_id(user_id):
        return Profissional.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def obter_todos():
        return Profissional.query.all()
    
    @staticmethod
    def criar(profissional_data):
        profissional = Profissional(**profissional_data)
        db.session.add(profissional)
        db.session.commit()
        return profissional
    
    @staticmethod
    def atualizar(profissional_id, profissional_data):
        profissional = Profissional.query.get(profissional_id)
        if profissional:
            for key, value in profissional_data.items():
                setattr(profissional, key, value)
            db.session.commit()
        return profissional