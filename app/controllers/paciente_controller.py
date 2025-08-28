from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from flask_cors import CORS
from app.services.chat_services import ChatService
from app.services.paciente_service import PacienteService
from app.utils.decorators import paciente_required, profissional_required
from app.utils.helpers import transactional
from app.models.paciente import Paciente
from app.models.profissional import Profissional    
from app.extensions import db

bp = Blueprint('api_paciente', __name__, url_prefix="/api")

@bp.route('/pacientes')
def listar_pacientes():
    """
    Lista todos os pacientes (apenas para profissionais)
    """
    try:
        pacientes = PacienteService.obter_todos_pacientes()
        pacientes_data = [{'id': p.id, 'nome': p.username} for p in pacientes]
        return jsonify(pacientes_data)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro ao carregar pacientes'}), 500
    
@bp.route('/pacientes/<int:paciente_id>/mensagens')
@login_required
def api_obter_mensagens_paciente(paciente_id):
    try:
        mensagens = ChatService.obter_mensagens_por_paciente(paciente_id)
        
        # Garanta que está enviando os campos corretos para a tabela
        mensagens_data = [{
            'id': m.id,
            'mensagem': m.mensagem,      # A mensagem do paciente
            'resposta': m.resposta,      # A resposta do profissional
            'timestamp': m.created_at.isoformat(),
            'enviadoPeloPaciente': m.eh_do_paciente 
        } for m in mensagens]
        
        return jsonify(mensagens_data)
        
    except Exception as e:
        print(f"ERRO em api_obter_mensagens_paciente: {e}")
        return jsonify({'error': 'Erro ao carregar mensagens do paciente'}), 500
    

@bp.route('/criar_pacientes', methods=['POST'])
@login_required
@profissional_required
def criar_paciente():
    dados = request.get_json()

    # 1. Validação dos dados recebidos
    username = dados.get('username')
    password = dados.get('password')

    if not username or not password:
        return jsonify({'error': 'Nome de usuário e senha são obrigatórios'}), 400

    # 2. Verificar se o username já existe
    if Paciente.query.filter_by(username=username).first():
        return jsonify({'error': 'Este nome de usuário já está em uso'}), 409 # 409 Conflict

    try:
        # 3. Criar a nova instância do Paciente
        novo_paciente = Paciente(username=username)

        # 4. Gerar o hash da senha
        novo_paciente.set_password(password)

        # 5. Associar ao profissional logado
        profissional_logado = Profissional.query.get(current_user.id) # Ou a lógica para obter o profissional
        if profissional_logado:
            novo_paciente.profissionais.append(profissional_logado)

        # 6. Salvar no banco de dados
        db.session.add(novo_paciente)
        db.session.commit()

        return jsonify({'message': 'Paciente criado com sucesso!', 'paciente_id': novo_paciente.id}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar paciente: {e}")
        return jsonify({'error': 'Erro interno ao criar paciente'}), 500
    



'''
@bp.route('/paciente/meu-perfil')
@login_required
@paciente_required
def meu_perfil():
    """
    Exibe o perfil do paciente logado
    """
    try:
        paciente = PacienteService.obter_paciente_por_user_id(current_user.id)
        if not paciente:
            flash('Perfil não encontrado', 'error')
            return redirect(url_for('auth.logout'))
        
        return render_template('paciente/meu_perfil.html', paciente=paciente)
    except Exception as e:
        flash('Erro ao carregar perfil', 'error')
        return redirect(url_for('diario.listar_diario'))

@bp.route('/paciente/editar', methods=['GET', 'POST'])
@login_required
@paciente_required
def editar_perfil():
    """
    Edita o perfil do paciente logado
    """
    try:
        paciente = PacienteService.obter_paciente_por_user_id(current_user.id)
        if not paciente:
            flash('Perfil não encontrado', 'error')
            return redirect(url_for('auth.logout'))
        
        if request.method == 'POST':
            dados = {
                'nome': request.form.get('nome'),
                'cpf': request.form.get('cpf'),
                'data_nascimento': request.form.get('data_nascimento'),
                'telefone': request.form.get('telefone')
            }
            
            paciente = PacienteService.atualizar_paciente(paciente.id, dados)
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('paciente.meu_perfil'))
        
        return render_template('paciente/editar.html', paciente=paciente)
        
    except Exception as e:
        flash('Erro ao editar perfil', 'error')
        return redirect(url_for('paciente.meu_perfil'))

@bp.route('/paciente/<int:paciente_id>')
@login_required
@profissional_required
def ver_paciente(paciente_id):
    """
    Visualiza detalhes de um paciente específico (apenas para profissionais)
    """
    try:
        paciente = PacienteService.obter_paciente_por_id(paciente_id)
        if not paciente:
            flash('Paciente não encontrado', 'error')
            return redirect(url_for('paciente.listar_pacientes'))
        
        # Obter registros do paciente
        from app.services import DiarioService
        registros = DiarioService.obter_registros_por_paciente(paciente_id)
        
        # Obter mensagens do chat
        from app.services import ChatService
        mensagens = ChatService.obter_mensagens_por_paciente(paciente_id)
        
        return render_template('paciente/detalhes.html', 
                             paciente=paciente, 
                             registros=registros,
                             mensagens=mensagens)
        
    except Exception as e:
        flash('Erro ao carregar dados do paciente', 'error')
        return redirect(url_for('paciente.listar_pacientes'))

@bp.route('/api/paciente/<int:paciente_id>')
@login_required
def api_obter_paciente(paciente_id):
    """
    API para obter dados de um paciente específico
    """
    try:
        # Verificar permissões
        if current_user.tipo == 'paciente':
            paciente_logado = PacienteService.obter_paciente_por_user_id(current_user.id)
            if paciente_logado.id != paciente_id:
                return jsonify({'error': 'Acesso não autorizado'}), 403
        
        paciente = PacienteService.obter_paciente_por_id(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        paciente_data = {
            'id': paciente.id,
            'nome': paciente.nome,
            'cpf': paciente.cpf,
            'data_nascimento': paciente.data_nascimento.isoformat() if paciente.data_nascimento else None,
            'telefone': paciente.telefone,
            'user_id': paciente.user_id
        }
        
        return jsonify(paciente_data)
    except Exception as e:
        return jsonify({'error': 'Erro ao carregar dados do paciente'}), 500
    
'''
# ... outras importações ...