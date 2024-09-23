from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from models import get_db_connection

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if not session.get('is_admin', False):
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'on'
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, senha, is_admin) VALUES (%s, %s, %s)',
                       (username, hashed_password, is_admin))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('usuarios.cadastro'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('cadastro.html', usuarios=usuarios)

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('is_admin', False):
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE idusuario = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('usuarios.cadastro'))

