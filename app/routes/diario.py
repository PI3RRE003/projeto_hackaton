from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import MensagemChat, Paciente, Profissional
from app.extensions import db
from datetime import date, datetime

diario_bp = Blueprint('diario', __name__)

@diario_bp.route('/diario')
@login_required
def listar_diario():
    # Pacientes veem apenas seus registros
    if current_user.tipo == 'paciente':
        paciente = Paciente.query.filter_by(user_id=current_user.id).first()
        mensagem = MensagemChat.query.filter_by(paciente_id=paciente.id).order_by(MensagemChat.data.desc()).all()
    # Profissionais veem todos os registros
    else:
        mensagem = MensagemChat.query.order_by(MensagemChat.data.desc()).all()
    
    return render_template('diario/listar.html', 
                         mensagem=mensagem)

@diario_bp.route('/diario/manha', methods=['GET', 'POST'])
@login_required
def registro_manha():
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        
        # Se for paciente, usa seu próprio ID
        if current_user.tipo == 'paciente':
            paciente = Paciente.query.filter_by(user_id=current_user.id).first()
            paciente_id = paciente.id
            profissional_id = None
        else:
            profissional = Profissional.query.filter_by(user_id=current_user.id).first()
            profissional_id = profissional.id
        
        # Verificar se já existe registro para hoje
        existing_record = MensagemChat.query.filter_by(
            paciente_id=paciente_id, 
            data=date.today()
        ).first()
        
        if existing_record:
            flash('Já existe um registro para esta manhã.', 'warning')
            return redirect(url_for('diario.registro_manha'))
        
        registro = MensagemChat(
            data=date.today(),
            paciente_id=paciente_id,
            profissional_id=profissional_id,
            registro=request.form.get('registro')
        )
        
        db.session.add(registro)
        db.session.commit()
        flash('Registro da manhã salvo com sucesso!', 'success')
        return redirect(url_for('diario.listar_diario'))
    
    # Se for profissional, precisa selecionar paciente
    pacientes = None
    if current_user.tipo == 'profissional':
        pacientes = Paciente.query.all()
    
    return render_template('diario/manha.html', pacientes=pacientes)

@diario_bp.route('/diario/tarde', methods=['GET', 'POST'])
@login_required
def registro_tarde():
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        
        if current_user.tipo == 'paciente':
            paciente = Paciente.query.filter_by(user_id=current_user.id).first()
            paciente_id = paciente.id
            profissional_id = None
        else:
            profissional = Profissional.query.filter_by(user_id=current_user.id).first()
            profissional_id = profissional.id
        
        existing_record = MensagemChat.query.filter_by(
            paciente_id=paciente_id, 
            data=date.today()
        ).first()
        
        if existing_record:
            flash('Já existe um registro para esta tarde.', 'warning')
            return redirect(url_for('diario.registro_tarde'))
        
        registro = MensagemChat(
            data=date.today(),
            paciente_id=paciente_id,
            profissional_id=profissional_id,
            registro=request.form.get('registro')
        )
        
        db.session.add(registro)
        db.session.commit()
        flash('Registro da tarde salvo com sucesso!', 'success')
        return redirect(url_for('diario.listar_diario'))
    
    pacientes = None
    if current_user.tipo == 'profissional':
        pacientes = Paciente.query.all()
    
    return render_template('diario/tarde.html', pacientes=pacientes)

@diario_bp.route('/diario/noite', methods=['GET', 'POST'])
@login_required
def registro_noite():
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        
        if current_user.tipo == 'paciente':
            paciente = Paciente.query.filter_by(user_id=current_user.id).first()
            paciente_id = paciente.id
            profissional_id = None
        else:
            profissional = Profissional.query.filter_by(user_id=current_user.id).first()
            profissional_id = profissional.id
        
        existing_record = MensagemChat.query.filter_by(
            paciente_id=paciente_id, 
            data=date.today()
        ).first()
        
        if existing_record:
            flash('Já existe um registro para esta noite.', 'warning')
            return redirect(url_for('diario.registro_noite'))
        
        registro = MensagemChat(
            data=date.today(),
            paciente_id=paciente_id,
            profissional_id=profissional_id,
            registro=request.form.get('registro')
        )
        
        db.session.add(registro)
        db.session.commit()
        flash('Registro da noite salvo com sucesso!', 'success')
        return redirect(url_for('diario.listar_diario'))
    
    pacientes = None
    if current_user.tipo == 'profissional':
        pacientes = Paciente.query.all()
    
    return render_template('diario/noite.html', pacientes=pacientes)

# API para verificar se já existe registro no dia
@diario_bp.route('/api/check_registro/<periodo>')
@login_required
def check_registro(periodo):
    paciente_id = request.args.get('paciente_id')
    
    if current_user.tipo == 'paciente':
        paciente = Paciente.query.filter_by(user_id=current_user.id).first()
        paciente_id = paciente.id
    
    today = date.today()
    
    if periodo == 'manha':
        exists = MensagemChat.query.filter_by(paciente_id=paciente_id, data=today).first()
    elif periodo == 'tarde':
        exists = MensagemChat.query.filter_by(paciente_id=paciente_id, data=today).first()
    elif periodo == 'noite':
        exists = MensagemChat.query.filter_by(paciente_id=paciente_id, data=today).first()
    else:
        return jsonify({'error': 'Período inválido'}), 400
    
    return jsonify({'exists': exists is not None})