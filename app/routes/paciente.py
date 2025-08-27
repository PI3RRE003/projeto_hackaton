from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.models import Paciente, User
from app.instance.database import db

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/pacientes')
@login_required
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('paciente/listar.html', pacientes=pacientes)

@paciente_bp.route('/paciente/novo', methods=['GET', 'POST'])
@login_required
def criar_paciente():
    if request.method == 'POST':
        # Processar formulário e salvar paciente
        pass
    return render_template('paciente/criar.html')

@paciente_bp.route('/paciente/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    # Processar edição
    return render_template('paciente/editar.html', paciente=paciente)