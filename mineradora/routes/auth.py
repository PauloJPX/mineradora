
import os
from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import get_db_connection
from req import login_required
from tkinter import Tk
from tkinter.filedialog import askdirectory
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

        # Verifica se o usuário existe e se a senha fornecida corresponde ao hash armazenado
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
        # Inicializar o Tkinter e ocultar a janela principal
        root = Tk()
        root.withdraw()

        # Abrir a caixa de diálogo para escolher o diretório
        backup_directory = askdirectory(title="Escolha o diretório para salvar o backup")

        # Verificar se o usuário escolheu um diretório
        if not backup_directory:
            flash("Nenhum diretório foi selecionado.", "danger")
            return redirect(url_for('auth.logout'))

        data_atual = datetime.now()
        file_name = f"copia{data_atual.strftime('%d%m%y')}.sql"

        # Definir o caminho completo para o arquivo de backup
        file_path = os.path.join(backup_directory, file_name)

        # Conectar ao banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Desativar as chaves estrangeiras
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Criar o arquivo de backup
        with open(file_path, "w") as f:
            for table in tables:
                table_name = table[0]
                print(f"Gerando backup para a tabela {table_name}...")

                # Gerar o CREATE TABLE
                create_table_sql = get_create_table(table_name)
                f.write(f"{create_table_sql};\n\n")

                # Gerar os INSERTs
                insert_statements = get_insert_statements(table_name)
                for insert_statement in insert_statements:
                    f.write(f"{insert_statement}\n")

                f.write("\n\n")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.close()
        connection.close()

        flash("Backup gerado com sucesso!", "success")
        return redirect(url_for('auth.login'))



@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()  # Limpa todas as variáveis de sessão
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

    # Verifica a senha atual
    cursor.execute('SELECT senha FROM usuarios WHERE idusuario = %s', (user_id,))
    user = cursor.fetchone()

    if user and check_password_hash(user['senha'], current_password):
        # Atualiza a senha com a nova senha encriptografada
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

    # Consulta para obter o comando CREATE TABLE da tabela
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    # O resultado da consulta está na segunda coluna, então acessamos [1]
    return result[1] if result else None


def get_insert_statements(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Consulta para obter todos os dados da tabela
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Obter os nomes das colunas da tabela
    columns = [desc[0] for desc in cursor.description]

    insert_statements = []
    for row in rows:
        # Criar um comando INSERT para cada linha de dados
        values = ', '.join([repr(value) if value is not None else "NULL" for value in row])
        insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});")

    cursor.close()
    connection.close()

    return insert_statements
