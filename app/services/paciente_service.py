from app.repositories.paciente_repository import PacienteRepository
from app.utils.helpers import transactional

class PacienteService:
    
    @staticmethod
    def obter_paciente_por_id(paciente_id):
        return PacienteRepository.obter_por_id(paciente_id)
    
    @staticmethod
    def obter_paciente_por_user_id(user_id):
        return PacienteRepository.obter_por_user_id(user_id)
    
    @staticmethod
    def obter_todos_pacientes():
        return PacienteRepository.obter_todos()
    
    @staticmethod
    @transactional
    def criar_paciente(dados_paciente):
        return PacienteRepository.criar(dados_paciente)
    
    @staticmethod
    @transactional
    def atualizar_paciente(paciente_id, dados_paciente):
        return PacienteRepository.atualizar(paciente_id, dados_paciente)
    
    @staticmethod
    @transactional
    def excluir_paciente(paciente_id):
        paciente = PacienteRepository.obter_por_id(paciente_id)
        if paciente:
            # TODO: Verificar se existem registros associados antes de excluir
            from app.extensions import db
            db.session.delete(paciente)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def buscar_pacientes_por_nome(nome):
        pacientes = PacienteRepository.obter_todos()
        return [p for p in pacientes if nome.lower() in p.nome.lower()]