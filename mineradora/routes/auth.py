from flask import Blueprint, request, redirect, url_for, session, render_template
from werkzeug.security import check_password_hash
from models import get_db_connection

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Mensagens de depuração
        print(f"Usuário encontrado: {user}")
        print(f"Senha fornecida: {password}")
        print(f"Senha armazenada: {user['senha']}")

        # Verifica se o usuário existe e se a senha fornecida corresponde ao hash armazenado
        if user and check_password_hash(user['senha'], password):
            session['logged_in'] = True
            session['user_id'] = user['idusuario']
            session['is_admin'] = user['is_admin']  # Define a sessão para admin
            return redirect(url_for('menu.menu_principal'))  # Redireciona para a página principal do menu
        else:
            return 'Credenciais inválidas', 401

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()  # Limpa todas as variáveis de sessão
    return redirect(url_for('auth.login'))  # Redireciona para a página de login


# Adiciona uma rota para a página principal/menu
@bp.route('/menu')
def menu_principal():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))

    # Renderiza a página principal ou menu com base na sessão do usuário
    return render_template('menu.html')  # Atualize com o nome correto do seu template de menu
