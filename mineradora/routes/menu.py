from flask import Blueprint, render_template, session

# Define o blueprint
bp = Blueprint('menu', __name__, url_prefix='/menu')

# Defina a função para obter os itens do menu
def get_menu_items(is_admin):
    menu_items = [
        {'name': 'Home', 'url': 'inicio.inicial'},
        {'name': 'Clientes', 'url': 'clientes.cadastro_cliente'},
        {'name': 'Vendas', 'url': 'vendas.incluir_venda'},  # Nova funcionalidade de vendas
        {'name': 'Logout', 'url': 'auth.logout'}

    ]

    if is_admin:
        menu_items.insert(0, {'name': 'Cadastro de Usuário', 'url': 'usuarios.cadastro'})

    return menu_items

# Rota para o menu principal
@bp.route('/')
def menu_principal():
    # Verifique se o usuário está autenticado e se é admin
    is_admin = session.get('is_admin', False)  # Obtém o valor de is_admin da sessão
    menu_items = get_menu_items(is_admin)
    return render_template('menu.html', menu_items=menu_items)
