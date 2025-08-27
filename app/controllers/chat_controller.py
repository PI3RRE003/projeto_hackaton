from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from app.extensions import db, socketio
from app.models import MensagemChat, Paciente, Profissional
from app.services.gpt_service import GPTService
from app.utils.decorators import paciente_required, profissional_required
from datetime import date


bp = Blueprint('chat', __name__)
gpt_service = GPTService()

@bp.route('/chat')
@login_required
def chat():
    if current_user.tipo == 'paciente':
        paciente = Paciente.query.filter_by(user_id=current_user.id).first()
        mensagens = MensagemChat.query.filter_by(paciente_id=paciente.id).order_by(MensagemChat.created_at.asc()).all()
        return render_template('chat.html', 
                             mensagens=mensagens, 
                             paciente=paciente,
                             pode_enviar=MensagemChat.pode_enviar_mensagem(paciente.id))
    else:
        # Profissionais veem todos os chats
        pacientes = Paciente.query.all()
        paciente_id = request.args.get('paciente_id')
        mensagens = []
        
        if paciente_id:
            mensagens = MensagemChat.query.filter_by(paciente_id=paciente_id).order_by(MensagemChat.created_at.asc()).all()
        
        return render_template('chat/profissional.html', 
                             mensagens=mensagens, 
                             pacientes=pacientes,
                             paciente_selecionado_id=paciente_id)

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        if current_user.tipo == 'paciente':
            paciente = Paciente.query.filter_by(user_id=current_user.id).first()
            join_room(f'paciente_{paciente.id}')
        else:
            join_room('profissionais')
        emit('status', {'message': 'Conectado'})

@socketio.on('enviar_mensagem')
@login_required
def handle_enviar_mensagem(data):
    try:
        if current_user.tipo != 'paciente':
            emit('erro', {'message': 'Apenas pacientes podem enviar mensagens'})
            return
        
        paciente = Paciente.query.filter_by(user_id=current_user.id).first()
        
        # Verificar limite de mensagens
        if not MensagemChat.pode_enviar_mensagem(paciente.id):
            emit('limite_atingido', {
                'message': 'Você atingiu o limite de 3 mensagens por dia. Volte amanhã para continuar.'
            })
            return
        
        mensagem = data.get('mensagem', '').strip()
        if not mensagem:
            emit('erro', {'message': 'Mensagem não pode estar vazia'})
            return
        
        # Salvar mensagem do paciente
        nova_mensagem = MensagemChat(
            paciente_id=paciente.id,
            mensagem=mensagem,
            eh_do_paciente=True,
            data=date.today()
        )
        
        db.session.add(nova_mensagem)
        db.session.commit()
        
        # Emitir mensagem para todas as salas relevantes
        emit('nova_mensagem', {
            'id': nova_mensagem.id,
            'mensagem': mensagem,
            'eh_do_paciente': True,
            'timestamp': nova_mensagem.created_at.isoformat(),
            'paciente_nome': paciente.nome
        }, room=f'paciente_{paciente.id}')
        
        emit('nova_mensagem', {
            'id': nova_mensagem.id,
            'mensagem': mensagem,
            'eh_do_paciente': True,
            'timestamp': nova_mensagem.created_at.isoformat(),
            'paciente_nome': paciente.nome,
            'paciente_id': paciente.id
        }, room='profissionais')
        
        # Gerar resposta do GPT
        resposta_gpt = gpt_service.gerar_resposta(mensagem)
        
        # Salvar resposta do GPT
        resposta_mensagem = MensagemChat(
            paciente_id=paciente.id,
            mensagem=mensagem,
            resposta=resposta_gpt,
            eh_do_paciente=False,
            data=date.today()
        )
        
        db.session.add(resposta_mensagem)
        db.session.commit()
        
        # Emitir resposta do GPT
        emit('nova_mensagem', {
            'id': resposta_mensagem.id,
            'mensagem': resposta_gpt,
            'eh_do_paciente': False,
            'timestamp': resposta_mensagem.created_at.isoformat(),
            'paciente_nome': 'Assistente Virtual'
        }, room=f'paciente_{paciente.id}')
        
        emit('nova_mensagem', {
            'id': resposta_mensagem.id,
            'mensagem': resposta_gpt,
            'eh_do_paciente': False,
            'timestamp': resposta_mensagem.created_at.isoformat(),
            'paciente_nome': 'Assistente Virtual',
            'paciente_id': paciente.id
        }, room='profissionais')
        
    except Exception as e:
        current_app.logger.error(f"Erro ao processar mensagem: {e}")
        emit('erro', {'message': 'Erro interno do servidor'})

@bp.route('/api/chat/status')
@login_required
@paciente_required
def chat_status():
    paciente = Paciente.query.filter_by(user_id=current_user.id).first()
    mensagens_hoje = MensagemChat.get_mensagens_hoje(paciente.id)
    pode_enviar = MensagemChat.pode_enviar_mensagem(paciente.id)
    
    return jsonify({
        'mensagens_hoje': mensagens_hoje,
        'limite': 3,
        'pode_enviar': pode_enviar
    })

# Chat API sem depender de sessão/cookies
@bp.route('/api/chat', methods=['POST'])
def chat_post():
    data = request.get_json()
    mensagem = data.get('mensagem')

    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    user_id = data.get("user_id")
    tipo = data.get("tipo")
    mensagem = data.get("message", "").strip()

    if not user_id or not tipo or not mensagem:
        return jsonify({"error": "user_id, tipo e message são obrigatórios"}), 400

    # Valida usuário
    if tipo == "profissional":
        user = Profissional.query.get(user_id)
    else:
        user = Paciente.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Aqui você integra com GPTService
    from app.services.gpt_service import GPTService
    gpt_service = GPTService()
    resposta_gpt = gpt_service.gerar_resposta(mensagem)

    # Retorna direto a resposta
    return jsonify({
        "user_message": mensagem,
        "assistant_response": resposta_gpt
    }), 200