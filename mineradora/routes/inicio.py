from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import get_db_connection

bp = Blueprint('inicio', __name__, url_prefix='/inicio')


@bp.route('/inicial', methods=['GET', 'POST'])
def inicial():
    return render_template('inicial.html')
