# Mude a importação do modelo antigo para o novo
from app.models import MensagemChat, Paciente 

class ChatService:

    @staticmethod
    def obter_mensagens_por_paciente(paciente_id):
        """
        Obtém o histórico de mensagens de um paciente, ordenado por data.
        """
        try:
            # A nova consulta filtra por paciente_id e ordena pela data de criação
            mensagens = MensagemChat.query.filter_by(
                paciente_id=paciente_id
            ).order_by(MensagemChat.created_at.asc()).all()
            
            return mensagens
        except Exception as e:
            print(f"Erro no ChatService ao obter mensagens: {e}")
            raise e