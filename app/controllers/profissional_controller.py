from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from flask_cors import CORS
from app.services.profissional_service import ProfissionalService
from app.utils.decorators import profissional_required

bp = Blueprint('profissional', __name__,url_prefix="/profissional")
CORS(bp)
@bp.route('/profissionais')

def listar_profissionais():
    """
    Lista todos os profissionais (apenas para profissionais)
    """
    try:
        profissionais = ProfissionalService.obter_todos_profissionais()
        return render_template('profissional/listar.html', profissionais=profissionais)
    except Exception as e:
        flash('Erro ao carregar lista de profissionais', 'error')
        return redirect(url_for('diario.listar_diario'))

@bp.route('/profissional/meu-perfil')
@login_required
@profissional_required
def meu_perfil():
    """
    Exibe o perfil do profissional logado
    """
    try:
        profissional = ProfissionalService.obter_profissional_por_user_id(current_user.id)
        if not profissional:
            flash('Perfil não encontrado', 'error')
            return redirect(url_for('auth.logout'))
        
        # Estatísticas (opcional)
        from app.services import DiarioService, PacienteService
        total_pacientes = len(PacienteService.obter_todos_pacientes())
        total_registros = len(DiarioService.obter_todos_registros())
        
        return render_template('profissional/meu_perfil.html', 
                             profissional=profissional,
                             total_pacientes=total_pacientes,
                             total_registros=total_registros)
    except Exception as e:
        flash('Erro ao carregar perfil', 'error')
        return redirect(url_for('diario.listar_diario'))

@bp.route('/profissional/editar', methods=['GET', 'POST'])
def editar_perfil():
    """
    Edita o perfil do profissional logado
    """
    try:
        profissional = ProfissionalService.obter_profissional_por_user_id(current_user.id)
        if not profissional:
            flash('Perfil não encontrado', 'error')
            return redirect(url_for('auth.logout'))
        
        if request.method == 'POST':
            dados = {
                'nome': request.form.get('nome'),
                'especialidade': request.form.get('especialidade'),
                'registro_profissional': request.form.get('registro_profissional')
            }
            
            profissional = ProfissionalService.atualizar_profissional(profissional.id, dados)
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('profissional.meu_perfil'))
        
        return render_template('profissional/editar.html', profissional=profissional)
        
    except Exception as e:
        flash('Erro ao editar perfil', 'error')
        return redirect(url_for('profissional.meu_perfil'))

@bp.route('/profissional/<int:profissional_id>')

def ver_profissional(profissional_id):
    """
    Visualiza detalhes de um profissional específico
    """
    try:
        profissional = ProfissionalService.obter_profissional_por_id(profissional_id)
        if not profissional:
            flash('Profissional não encontrado', 'error')
            return redirect(url_for('profissional.listar_profissionais'))
        
        # Obter registros feitos por este profissional
        from app.services import DiarioService
        registros = DiarioService.obter_registros_por_profissional(profissional_id)
        
        return render_template('profissional/detalhes.html', 
                             profissional=profissional, 
                             registros=registros)
        
    except Exception as e:
        flash('Erro ao carregar dados do profissional', 'error')
        return redirect(url_for('profissional.listar_profissionais'))

@bp.route('/api/profissionais')
@login_required
def api_listar_profissionais():
    """
    API para listar profissionais
    """
    try:
        profissionais = ProfissionalService.obter_todos_profissionais()
        profissionais_data = [{
            'id': p.id,
            'nome': p.nome,
            'especialidade': p.especialidade,
            'registro_profissional': p.registro_profissional
        } for p in profissionais]
        
        return jsonify(profissionais_data)
    except Exception as e:
        return jsonify({'error': 'Erro ao carregar profissionais'}), 500

@bp.route('/api/profissional/<int:profissional_id>')
@login_required
def api_obter_profissional(profissional_id):
    """
    API para obter dados de um profissional específico
    """
    try:
        profissional = ProfissionalService.obter_profissional_por_id(profissional_id)
        if not profissional:
            return jsonify({'error': 'Profissional não encontrado'}), 404
        
        profissional_data = {
            'id': profissional.id,
            'nome': profissional.nome,
            'especialidade': profissional.especialidade,
            'registro_profissional': profissional.registro_profissional,
            'user_id': profissional.user_id
        }
        
        return jsonify(profissional_data)
    except Exception as e:
        return jsonify({'error': 'Erro ao carregar dados do profissional'}), 500

@bp.route('/dashboard')
@login_required
@profissional_required
def dashboard():
    """
    Dashboard para profissionais com estatísticas e resumo
    """
    try:
        from app.services import (
            PacienteService, 
            DiarioService, 
            ChatService,
            ProfissionalService
        )
        
        profissional = ProfissionalService.obter_profissional_por_user_id(current_user.id)
        
        # Estatísticas
        total_pacientes = len(PacienteService.obter_todos_pacientes())
        total_registros = len(DiarioService.obter_todos_registros())
        registros_hoje = len(DiarioService.obter_registros_hoje())
        total_mensagens = len(ChatService.obter_todas_mensagens())
        
        # Últimos registros
        ultimos_registros = DiarioService.obter_ultimos_registros(5)
        
        # Pacientes com registros pendentes
        pacientes_pendentes = DiarioService.obter_pacientes_com_registros_pendentes()
        
        return render_template('profissional/dashboard.html',
                             profissional=profissional,
                             total_pacientes=total_pacientes,
                             total_registros=total_registros,
                             registros_hoje=registros_hoje,
                             total_mensagens=total_mensagens,
                             ultimos_registros=ultimos_registros,
                             pacientes_pendentes=pacientes_pendentes)
        
    except Exception as e:
        flash('Erro ao carregar dashboard', 'error')
        return redirect(url_for('diario.listar_diario'))




from app.models.paciente import Paciente
from app.models.chat import MensagemChat
@bp.route('/api/mensagens/<int:paciente_id>', methods=['GET'])
def profissional_ver_mensagens(paciente_id):
    # opcional: verificar se o profissional atende esse paciente
    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({"error": "Paciente não encontrado"}), 404

    mensagens = MensagemChat.query.filter_by(paciente_id=paciente_id).order_by(MensagemChat.timestamp.asc()).all()
    resultado = [
        {
            "id": msg.id,
            "conteudo": msg.conteudo,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in mensagens
    ]

    return jsonify({"mensagens": resultado}), 200