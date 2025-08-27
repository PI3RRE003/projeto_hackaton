from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Profissional
from app.instance.database import db

profissional_bp = Blueprint('profissional', __name__)

@profissional_bp.route('/profissionais')
@login_required
def listar_profissionais():
    profissionais = Profissional.query.all()
    return render_template('profissional/listar.html', profissionais=profissionais)

@profissional_bp.route('/profissional/novo', methods=['GET', 'POST'])
@login_required
def criar_profissional():
    if request.method == 'POST':
        # Processar formulário e salvar profissional
        pass
    return render_template('profissional/criar.html')

@profissional_bp.route('/profissional/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    # Processar edição
    return render_template('profissional/editar.html', profissional=profissional)