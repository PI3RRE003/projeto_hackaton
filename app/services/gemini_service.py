from google import genai
from app.config import Config

class GeminiService:
    def __init__(self):        
        client = genai.Client(api_key=Config.GEMINIAI_API_KEY)
        self.client = client
    def gerar_resposta(self, mensagem, contexto=None):
       
        try:
            # Contexto para o GPT (pode ser personalizado)
            prompt = f"""
            Você é um assistente de saúde mental. Responda de forma empática e profissional.
            
            Mensagem do paciente: {mensagem}
            
            Responda de forma acolhedora, oferecendo apoio e, se necessário, sugerindo
            que o paciente compartilhe mais detalhes com seu profissional de saúde.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=prompt
            )
            
            return response.text
        
        except Exception as e:
            print(f"Erro ao chamar API: {e}")
            return "Desculpe, estou tendo dificuldades técnicas no momento. Por favor, tente novamente mais tarde ou entre em contato com seu profissional de saúde."
        


