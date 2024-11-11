from flask import Blueprint, render_template, session
from models import get_db_connection
from req import login_required

# Define o blueprint
bp = Blueprint('menu', __name__, url_prefix='/menu')

# Defina a função para obter os itens do menu
def get_menu_items(is_admin,id_usuario):
    if not(is_admin):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('select m.nome_modulo from acesso a,usuarios u'
                       ',modulo m where  a.idusuario = u.idusuario and a.idmodulo = m.idmodulo and u.idusuario = %s', (id_usuario,))
        itensdomenu = cursor.fetchall()

        menu_items = []
        for item in itensdomenu:
            nomeitem = (item['nome_modulo'])
            if nomeitem == 'Home':
                menu_items.append({'name': 'Home', 'url': 'inicio.inicial'})
            if nomeitem == 'Clientes':
                menu_items.append({'name': 'Clientes', 'url': 'clientes.cadastro_cliente'})

            if nomeitem == 'Caminhões':
                menu_items.append({'name': 'Caminhões', 'url': 'caminhoes.cadastro_caminhao'})

            if nomeitem == 'Produtos':
                menu_items.append({'name': 'Produtos', 'url': 'produtos.cadastro_produto'})

            if nomeitem == 'Vendas':
                menu_items.append({'name': 'Vendas', 'url': 'vendas.incluir_venda'})

            if nomeitem == 'Entregas':
                menu_items.append({'name': 'Entregas', 'url': 'entregas.incluir_entrega'})

            if nomeitem == 'Consultas':
                menu_items.append({'name': 'Consultas', 'url': 'consultas.pagina_consultas'})

            if nomeitem == 'Acessos':
                menu_items.append({'name': 'Acessos', 'url': 'acesso.cadastro_acesso'})
    else:
           menu_items = [
           {'name': 'Cadastro de Usuário', 'url': 'usuarios.cadastro'},
           {'name': 'Home', 'url': 'inicio.inicial'},
           {'name': 'Clientes', 'url': 'clientes.cadastro_cliente'},
           {'name': 'Caminhões', 'url': 'caminhoes.cadastro_caminhao'},  # Nome correto para o cadastro de caminhões
           {'name': 'Produtos', 'url': 'produtos.cadastro_produto'},
           {'name': 'Vendas', 'url': 'vendas.incluir_venda'},  # Nova funcionalidade de vendas
           {'name': 'Entregas', 'url': 'entregas.incluir_entrega'}, # nova funcionalidade de entregas
           {'name': 'Consultas', 'url': 'consultas.pagina_consultas'}, # aqui vai chamar html com varios botoes
           {'name': 'Acessos', 'url': 'acesso.cadastro_acesso'},
           ]
    menu_items.append({'name': 'Logout', 'url': 'auth.logout'})
    return menu_items

# Rota para o menu principal
@bp.route('/')
@login_required
def menu_principal():
    # Verifique se o usuário está autenticado e se é admin
    is_admin = session.get('is_admin', False)  # Obtém o valor de is_admin da sessão
    id_usuario = session.get('user_id')
    menu_items = get_menu_items(is_admin,id_usuario)
    return render_template('menu.html', menu_items=menu_items)


