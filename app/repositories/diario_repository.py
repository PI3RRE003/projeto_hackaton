from app.extensions import db
from app.models import Registro
from datetime import date

class DiarioRepository:
    @staticmethod
    def criar_registro(data):
        registro = Registro(**data)
        db.session.add(registro)
        db.session.commit()
        return registro
    
    @staticmethod
    def atualizar_registro(registro_id, data):
        registro = Registro.query.get(registro_id)
        if registro:
            for key, value in data.items():
                setattr(registro, key, value)
            db.session.commit()
        return registro
    
    @staticmethod
    def obter_registro_por_id(registro_id):
        return Registro.query.get(registro_id)
    
    @staticmethod
    def obter_registro_hoje(paciente_id):
        hoje = date.today()
        return Registro.query.filter_by(paciente_id=paciente_id, data=hoje).first()
    
    @staticmethod
    def obter_registros_por_paciente(paciente_id):
        return Registro.query.filter_by(paciente_id=paciente_id).order_by(Registro.data.desc()).all()
    
    @staticmethod
    def obter_todos_registros():
        return Registro.query.order_by(Registro.data.desc()).all()
    
    @staticmethod
    def existe_registro_hoje(paciente_id):
        hoje = date.today()
        return Registro.query.filter_by(paciente_id=paciente_id, data=hoje).first() is not None