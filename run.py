from app.app import create_app
from dotenv import load_dotenv
from app.extensions import db, socketio
from app.models.paciente import Paciente 
from app.models.profissional import Profissional 
from app.models.chat import MensagemChat
from datetime import datetime, timedelta
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
app = create_app()

        
    # --- Comandos para o CLI do Flask ---
# Estes comandos ajudam a gerenciar o banco de dados e a popular dados de teste.
# Para usá-los, execute no terminal:
# flask init-db
# flask create-test-data
# flask reset-db

@app.cli.command("init-db")
def init_db():
    """
    Inicializa o banco de dados: apaga as tabelas existentes e cria novas.
    Isso garante um estado limpo para começar.
    """
    print("Iniciando a inicialização do banco de dados...")
    print("Removendo todas as tabelas existentes (se houver)...")
    db.drop_all()
    print("Criando todas as tabelas com base nos modelos...")
    db.create_all()
    print("Banco de dados inicializado com sucesso! ✨")
    print("Para popular com dados de teste, execute: flask create-test-data")

@app.cli.command("create-test-data")
def create_test_data():
    """
    Cria dados de teste (paciente, profissional e mensagens) no banco de dados.
    Útil para testar a aplicação sem precisar cadastrar tudo manualmente.
    """
    try:
        print("Criando dados de teste...")
        
        # Criar um paciente de teste com nome e credenciais
        paciente = Paciente(
            username='PACIENTE'
        )
        paciente.set_password('senha123') # Define a senha de forma segura
        
        # Criar um profissional de teste com nome e credenciais
        profissional = Profissional(
            username='PROFISSIONAL'
        )
        profissional.set_password('senha123') # Define a senha de forma segura
        
        # Adiciona os novos registros à sessão do banco de dados
        db.session.add(paciente)
        db.session.add(profissional)
        
        # Comita (salva) as mudanças no banco de dados para que os IDs sejam gerados
        db.session.commit()
        
        print("Perfis de paciente e profissional criados com sucesso.")
        
        # Criar mensagens de exemplo associadas ao paciente criado
        mensagem1 = MensagemChat(
            paciente_id=paciente.id, # Usa o ID do paciente recém-criado
            mensagem="Estou me sentindo muito ansioso hoje.",
            resposta="Entendo que deve ser difícil. Lembre-se de praticar a respiração profunda.",
            eh_do_paciente=True,
            data=datetime.now().date()
        )
        
        mensagem2 = MensagemChat(
            paciente_id=paciente.id, # Usa o ID do paciente recém-criado
            mensagem="Tive dificuldade para dormir esta noite.",
            resposta="A insônia pode estar relacionada à ansiedade. Tente criar uma rotina relaxante.",
            eh_do_paciente=True,
            data=datetime.now().date()
        )
        
        # Adiciona as mensagens à sessão
        db.session.add(mensagem1)
        db.session.add(mensagem2)
        
        # Comita as mensagens no banco de dados
        db.session.commit()
        
        print("Mensagens de exemplo criadas.")
        print("\n--- Dados de Teste Criados com Sucesso! ---")
        print(f"👤 Paciente: username='paciente', password='senha123', nome='{paciente.username}'")
        print(f"🩺 Profissional: username='profissional', password='senha123', nome='{profissional.username}'")
        print("💬 2 mensagens de chat de exemplo foram adicionadas para o paciente.")
        
    except Exception as e:
        # Em caso de erro, desfaz a transação para não deixar o banco em estado inconsistente
        db.session.rollback()
        print(f"❌ Erro ao criar dados de teste: {e}")
        # Relança a exceção para que o Flask possa capturá-la e exibir mais detalhes
        raise e

@app.cli.command("reset-db")
def reset_db():
    """
    Um atalho para apagar e recriar o banco de dados.
    Equivalente a executar 'flask init-db'.
    """
    init_db()

# --- Ponto de Entrada da Aplicação ---
# O bloco a seguir só será executado se este script for chamado diretamente
# (ex: python run.py), e não quando for importado.
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento com SocketIO e modo de depuração ativado
    socketio.run(app, debug=True)

    
    # Criar algumas mensagens de exemplo
    from datetime import datetime, timedelta
    
    mensagem1 = MensagemChat(
        paciente_id=Paciente.id,
        mensagem="Estou me sentindo muito ansioso hoje.",
        resposta="Entendo que deve ser difícil. Lembre-se de praticar a respiração profunda. Quer compartilhar mais sobre o que está sentindo?",
        eh_do_paciente=True,
        data=datetime.now().date()
    )
    
    mensagem2 = MensagemChat(
        paciente_id=Paciente.id,
        mensagem="Tive dificuldade para dormir esta noite.",
        resposta="A insônia pode ser relacionada à ansiedade. Tente criar uma rotina relaxante antes de dormir. Conte mais para seu profissional na próxima consulta.",
        eh_do_paciente=True,
        data=datetime.now().date()
    )
    
    db.session.add(mensagem1)
    db.session.add(mensagem2)
    db.session.commit()
    
    print("Test data created.")

if __name__ == '__main__':
    socketio.run(app, debug=True)