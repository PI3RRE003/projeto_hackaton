import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-segura'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações do OpenAI GPT
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'sua-chave-openai-aqui'
    GEMINIAI_API_KEY = os.environ.get('GEMINIAI_API_KEY') or 'sua-chave-gemini-aqui'
    
    # Configurações do WebSocket
    SOCKETIO_ASYNC_MODE = 'threading'