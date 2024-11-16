from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import get_db_connection
#from app import login_required  # Importa o decorador

bp = Blueprint('vendas', __name__, url_prefix='/vendas')

@bp.route('/incluir', methods=['GET', 'POST'])
#@login_required  # Protege a rota
def incluir_venda():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Captura os dados do formulário
        numerovenda = int(request.form['numerovenda'])
        data_venda = request.form['data_venda']
        cliente_id = request.form['cliente_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])
        valor_produto = float(request.form['valor_produto'])
        valor_negociado = float(request.form['valor_negociado'])
        valor_frete = float(request.form['valor_frete']) if request.form['valor_frete'] else 0.0

        valor_total = valor_negociado * quantidade + valor_frete

        cursor.execute(''' 
            INSERT INTO vendas (numerovenda, idcliente, idproduto, data_venda, quantidade, valor_produto, valor_produto_negociado, valor_frete, valor_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (numerovenda, cliente_id, produto_id, data_venda, quantidade, valor_produto, valor_negociado, valor_frete, valor_total))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('vendas.incluir_venda', teste='sim', msg='Venda Incluida com Sucesso'))

    cursor.execute("SELECT idcliente, razao_social FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT idproduto, descricao, preco_de_venda FROM produtos")
    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('incluir_venda.html', clientes=clientes, produtos=produtos)

@bp.route('/verificar_numerovenda/<int:numerovenda>', methods=['GET'])

def verificar_numerovenda(numerovenda):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vendas WHERE numerovenda = %s", (numerovenda,))
    venda_existente = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({"existe": venda_existente is not None, "venda": venda_existente})

@bp.route('/excluir_venda', methods=['POST'])

def excluir_venda():
    numerovenda = request.form['numerovenda_excluir']
    retorno = verificar_numerovenda(numerovenda) # essa fucao retorna um jso
    resposta = retorno.json["existe"]
    if resposta:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE numerovenda = %s", (numerovenda,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('vendas.incluir_venda', teste='sim', msg='Venda excluida com Sucesso'))
    else:
        return redirect(url_for('vendas.incluir_venda', teste='sim', msg='Venda nao existia'))