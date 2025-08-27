from app.repositories.diario_repository import DiarioRepository
from app.models.paciente import Paciente
from datetime import date

class DiarioService:
    @staticmethod
    def criar_registro_diario(paciente_id, profissional_id, periodo, dados):
        registro_hoje = DiarioRepository.obter_registro_hoje(paciente_id)
        
        if registro_hoje:
            # Atualizar registro existente
            campos_atualizar = {}
            if periodo == 'manha':
                campos_atualizar = {
                    'registro': dados.get('registro')}
            elif periodo == 'tarde':
                campos_atualizar = {
                    'registro': dados.get('registro')}
            elif periodo == 'noite':
                campos_atualizar = {
                    'registro': dados.get('registro')}
            
            return DiarioRepository.atualizar_registro(registro_hoje.id, campos_atualizar)
        else:
            # Criar novo registro
            dados_registro = {
                'paciente_id': paciente_id,
                'profissional_id': profissional_id,
                'data': date.today()
            }
            
            if periodo == 'manha':
                dados_registro.update({
                    'registro': dados.get('registro')
                })
            elif periodo == 'tarde':
                dados_registro.update({
                    'registro': dados.get('registro')
                })
            elif periodo == 'noite':
                dados_registro.update({
                    'registro': dados.get('registro')                })
            
            return DiarioRepository.criar_registro(dados_registro)
    
    @staticmethod
    def obter_registros_usuario(current_user):
        if current_user.tipo == 'paciente':
            paciente = Paciente.query.filter_by(user_id=current_user.id).first()
            return DiarioRepository.obter_registros_por_paciente(paciente.id)
        else:
            return DiarioRepository.obter_todos_registros()
    
    @staticmethod
    def verificar_registro_periodo(paciente_id, periodo):
        registro = DiarioRepository.obter_registro_hoje(paciente_id)
        if not registro:
            return False
        
        if periodo == 'manha':
            return registro.manha_sono is not None
        elif periodo == 'tarde':
            return registro.tarde_atividades is not None
        elif periodo == 'noite':
            return registro.noite_janta is not None
        
        return False