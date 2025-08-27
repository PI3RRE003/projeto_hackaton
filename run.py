from app.app import create_app
from dotenv import load_dotenv
from app.extensions import db, socketio
from app.models.paciente import Paciente 
from app.models.profissional import Profissional 
from app.models.chat import MensagemChat
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


app = create_app()

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    print("Removendo tabelas existentes...")
    db.drop_all()  # CRÍTICO: Adicionar esta linha
    print("Criando novas tabelas...")
    db.create_all()
    print("Database initialized successfully!")

@app.cli.command("create-test-data")
def create_test_data():
    """Create test data."""
    try:
        print("Criando dados de teste...")
        
        # Criar usuários de teste
        paciente_user = Paciente(username='paciente')
        paciente_user.set_password('senha123')
        
        profissional_user = Profissional(username='profissional')
        profissional_user.set_password('senha123')
        
        db.session.add_all([paciente_user, profissional_user])
        db.session.commit()
        
        print("Usuários criados...")
        
        # Criar paciente
        paciente = Paciente(
            username='João da Silva',
            user_id=paciente_user.id
        )
        
        # Criar profissional
        profissional = Profissional(
            username='Dra. Maria Santos',
            user_id=profissional_user.id
        )
        
        db.session.add(paciente)
        db.session.add(profissional)
        db.session.commit()
        
        print("Perfis criados...")
        
        # Criar algumas mensagens de exemplo
        from datetime import datetime, timedelta
        
        mensagem1 = MensagemChat(
            paciente_id=paciente.id,
            mensagem="Estou me sentindo muito ansioso hoje.",
            resposta="Entendo que deve ser difícil. Lembre-se de praticar a respiração profunda. Quer compartilhar mais sobre o que está sentindo?",
            eh_do_paciente=True,
            data=datetime.now().date()
        )
        
        mensagem2 = MensagemChat(
            paciente_id=paciente.id,
            mensagem="Tive dificuldade para dormir esta noite.",
            resposta="A insônia pode ser relacionada à ansiedade. Tente criar uma rotina relaxante antes de dormir. Conte mais para seu profissional na próxima consulta.",
            eh_do_paciente=True,
            data=datetime.now().date()
        )
        
        db.session.add(mensagem1)
        db.session.add(mensagem2)
        db.session.commit()
        
        print("Mensagens criadas...")
        print("Test data created successfully!")
        print("\nDados criados:")
        print("- Usuário paciente: paciente / senha123")
        print("- Usuário profissional: profissional / senha123")
        print("- Perfil paciente: João da Silva")
        print("- Perfil profissional: Dra. Maria Santos")
        print("- 2 mensagens de exemplo")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar dados de teste: {e}")
        raise e

@app.cli.command("reset-db")
def reset_db():
    """Reset database - drop all tables and recreate them."""
    print("Resetando banco de dados...")
    db.drop_all()
    db.create_all()
    print("Banco resetado! Execute 'flask create-test-data' para criar dados de teste.")

if __name__ == '__main__':
    socketio.run(app, debug=True)
@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized.")

@app.cli.command("create-test-data")
def create_test_data():
    """Create test data."""
    # Criar usuários de teste
    paciente_user = Paciente(username='paciente')
    paciente_user.set_password('senha123')
    
    profissional_user = Profissional(username='profissional')
    profissional_user.set_password('senha123')
    
    db.session.add_all([paciente_user,profissional_user])
    db.session.commit()
    
    # Criar paciente
    paciente = Paciente(
        username='João da Silva',
        user_id=paciente_user.id
    )
    
    # Criar profissional
    profissional = Profissional(
        username='Dra. Maria Santos',
        user_id=profissional_user.id
    )
    
    db.session.add(paciente)
    db.session.add(profissional)
    db.session.commit()# -*- coding: utf-8 -*-

# Importações necessárias do sistema e bibliotecas
import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Importações dos componentes da sua aplicação Flask
# É uma boa prática agrupar as importações da aplicação
from app.app import create_app
from app.extensions import db, socketio
from app.models.paciente import Paciente 
from app.models.profissional import Profissional 
from app.models.chat import MensagemChat

# Obtém a chave da API da OpenAI das variáveis de ambiente
# Embora não seja usada neste script, é uma boa prática mantê-la aqui se for usada em outro lugar
api_key = os.getenv("OPENAI_API_KEY")

# Cria a instância da aplicação Flask
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
            username='João da Silva'
        )
        paciente.set_password('senha123') # Define a senha de forma segura
        
        # Criar um profissional de teste com nome e credenciais
        profissional = Profissional(
            username='Dra. Maria Santos'
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