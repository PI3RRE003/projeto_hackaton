from app.repositories.profissional_repository import ProfissionalRepository
from app.utils.helpers import transactional

class ProfissionalService:
    
    @staticmethod
    def obter_profissional_por_id(profissional_id):
        return ProfissionalRepository.obter_por_id(profissional_id)
    
    @staticmethod
    def obter_profissional_por_user_id(user_id):
        return ProfissionalRepository.obter_por_user_id(user_id)
    
    @staticmethod
    def obter_todos_profissionais():
        return ProfissionalRepository.obter_todos()
    
    @staticmethod
    @transactional
    def criar_profissional(dados_profissional):
        return ProfissionalRepository.criar(dados_profissional)
    
    @staticmethod
    @transactional
    def atualizar_profissional(profissional_id, dados_profissional):
        return ProfissionalRepository.atualizar(profissional_id, dados_profissional)
    
    @staticmethod
    @transactional
    def excluir_profissional(profissional_id):
        profissional = ProfissionalRepository.obter_por_id(profissional_id)
        if profissional:
            # TODO: Verificar se existem registros associados antes de excluir
            from app.extensions import db
            db.session.delete(profissional)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def buscar_profissionais_por_especialidade(especialidade):
        profissionais = ProfissionalRepository.obter_todos()
        return [p for p in profissionais if especialidade.lower() in p.especialidade.lower()]