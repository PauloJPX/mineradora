#consultas.py
from flask import Blueprint, render_template

bp = Blueprint('consultas', __name__)

@bp.route('/consultas')
def exibir_consultas():
    return render_template('consultas.html')
