# funcao de conexa e de pegar os itens do menu
import mysql.connector
from config import Config
from flask import session

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    return conn

# Função para obter os itens do menu
def get_menu_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obter se o usuário é admin
    is_admin = session.get('is_admin', False)
    idusuario = session.get('idusuario')

    # Consulta para obter os itens do menu
    if is_admin:
        cursor.execute("SELECT nome_modulo, rota FROM modulo")
    else:
        query = """
        SELECT m.nome_modulo, m.rota
        FROM modulo m
        JOIN acesso a ON m.idmodulo = a.idmodulo
        WHERE a.idusuario = %s
        """
        cursor.execute(query, (idusuario,))

    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return menu_items

