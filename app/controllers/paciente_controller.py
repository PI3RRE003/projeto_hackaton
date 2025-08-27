from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from flask_cors import CORS
from app.services.paciente_service import PacienteService
from app.utils.decorators import paciente_required, profissional_required
from app.utils.helpers import transactional

bp = Blueprint('paciente', __name__, url_prefix="/paciente")
CORS(bp)
@bp.route('/pacientes')
@login_required
@profissional_required
def listar_pacientes():
    """
    Lista todos os pacientes (apenas para profissionais)
    """
    try:
        pacientes = PacienteService.obter_todos_pacientes()
        return render_template('paciente/listar.html', pacientes=pacientes)
    except Exception as e:
        flash('Erro ao carregar lista de pacientes', 'error')
        return redirect(url_for('diario.listar_diario'))

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

@bp.route('/api/pacientes')
@login_required
@profissional_required
def api_listar_pacientes():
    """
    API para listar pacientes (usado para selects e autocomplete)
    """
    try:
        pacientes = PacienteService.obter_todos_pacientes()
        pacientes_data = [{
            'id': p.id,
            'nome': p.nome,
            'cpf': p.cpf,
            'telefone': p.telefone
        } for p in pacientes]
        
        return jsonify(pacientes_data)
    except Exception as e:
        return jsonify({'error': 'Erro ao carregar pacientes'}), 500

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