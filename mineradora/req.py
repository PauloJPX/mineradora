#req.py sera usado para requisicoes,tanto de login oou de acesso

from flask import session, redirect, url_for
from functools import wraps
from models import get_db_connection  # Ajuste para o seu método de conexão com o banco


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function




def pode(modulo_nome):
    """
    Decorador que verifica se o usuário tem permissão para acessar um módulo específico.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verifica se o usuário está logado
            if 'logged_in' not in session:
                return redirect(url_for('auth.login'))

            # Obtém o id do usuário da sessão
            id_usuario = session.get('user_id')  # Supondo que você armazene o id do usuário na sessão

            e_admin = session.get('is_admin')
            if not e_admin:
                # Conecta ao banco de dados
                conn = get_db_connection()
                cursor = conn.cursor(dictionary=True)

                # Consulta para verificar se o usuário tem acesso ao módulo
                cursor.execute('''SELECT m.nome_modulo 
                                  FROM acesso a
                                  JOIN usuarios u ON a.idusuario = u.idusuario
                                  JOIN modulo m ON a.idmodulo = m.idmodulo
                                  WHERE u.idusuario = %s AND m.nome_modulo = %s''',
                               (id_usuario, modulo_nome))

                # Verifica se o módulo foi encontrado

                acesso = cursor.fetchone()
                if not acesso:
                    # Se o usuário não tem acesso ao módulo, redireciona
                    return redirect(url_for('inicio.inicial'))  # Redireciona para uma página inicial ou qualquer outra

            # Caso tenha acesso ou seja admin, permite o acesso à rota
            return f(*args, **kwargs)

        return decorated_function

    return decorator


