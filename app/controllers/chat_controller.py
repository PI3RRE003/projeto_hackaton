from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user, login_manager
from flask_socketio import emit, join_room
from app.services.gemini_service import GeminiService
from app.utils.decorators import paciente_required, profissional_required
from datetime import date

bp = Blueprint('chat', __name__)
gemini_service = GeminiService()
'''

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
'''

@bp.route('/api/chat', methods=['POST'])
def chat_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado enviado no corpo da requisição"}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({"error": "O campo 'message' é obrigatório e não pode estar vazio"}), 400

        # Integra com GPTService
        try:
            from app.services.gemini_service import GeminiService
            gpt_service = GeminiService()
            resposta_gpt = gpt_service.gerar_resposta(message)
            return jsonify({
                "status": "success",
                "direcionamento": resposta_gpt
            }), 200
        except Exception as e:
            return jsonify({"error": f"Erro ao processar a mensagem com GPTService: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Erro interno no servidor: {str(e)}"}), 500    # Retorna direto a resposta
    '''
    return jsonify({
        "user_message": mensagem,
        "assistant_response": resposta_gpt
    }), 200
    '''