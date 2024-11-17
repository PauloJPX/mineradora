import os
from flask import Blueprint, request, redirect, url_for, session, render_template, flash, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from models import get_db_connection
from req import login_required
from datetime import datetime

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

        if user and check_password_hash(user['senha'], password):
            session['logged_in'] = True
            session['user_id'] = user['idusuario']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('menu.menu_principal'))
        else:
            flash('Credenciais inválidas', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@bp.route('/gerar_backup', methods=['GET', 'POST'])
@login_required
def gerar_backup():
    if request.method == 'POST':
        data_atual = datetime.now()
        file_name = f"copia{data_atual.strftime('%d%m%y')}.sql"
        file_path = os.path.join(os.getcwd(), file_name)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        with open(file_path, "w") as f:
            for table in tables:
                table_name = table[0]
                print(f"Gerando backup para a tabela {table_name}...")

                create_table_sql = get_create_table(table_name)
                f.write(f"{create_table_sql};\n\n")

                insert_statements = get_insert_statements(table_name)
                for insert_statement in insert_statements:
                    f.write(f"{insert_statement}\n")

                f.write("\n\n")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.close()
        connection.close()

        flash("Backup gerado com sucesso!", "success")

        # Retornar o arquivo para download
        return send_file(file_path, as_attachment=True)

    return redirect(url_for('auth.login'))


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()
        flash('Você saiu do sistema com sucesso.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('logout.html')


@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT senha FROM usuarios WHERE idusuario = %s', (user_id,))
    user = cursor.fetchone()

    if user and check_password_hash(user['senha'], current_password):
        hashed_password = generate_password_hash(new_password)
        cursor.execute('UPDATE usuarios SET senha = %s WHERE idusuario = %s', (hashed_password, user_id))
        conn.commit()
        flash('Senha alterada com sucesso!', 'success')
    else:
        flash('Senha atual incorreta. Tente novamente.', 'danger')

    cursor.close()
    conn.close()
    return redirect(url_for('auth.logout'))


def get_create_table(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[1] if result else None


def get_insert_statements(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    insert_statements = []
    for row in rows:
        values = ', '.join([repr(value) if value is not None else "NULL" for value in row])
        insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});")

    cursor.close()
    connection.close()

    return insert_statements
