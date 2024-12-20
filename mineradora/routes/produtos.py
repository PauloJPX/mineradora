# produtos.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import get_db_connection
from req import login_required,pode

bp = Blueprint('produtos', __name__, url_prefix='/produtos')


@bp.route('/cadastro_produto', methods=['GET', 'POST'])
@login_required
@pode('Produtos')
def cadastro_produto():
    if request.method == 'POST':
        descricao = request.form['descricao']
        nosso = request.form['nosso']
        preco_de_custo = request.form['preco_de_custo']
        preco_de_venda = request.form['preco_de_venda']
        produto_id = request.form.get('idproduto')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print(produto_id, nosso, preco_de_custo, preco_de_venda)
        print('**********************************************')
        print(produto_id, type(produto_id))

        if produto_id:  # Se idproduto  presente, realizar UPDATE
           print('entrei......')
           print(produto_id)
           print('++++++++++++++++++++')
           cursor.execute(
                'UPDATE produtos SET descricao=%s, nosso=%s, preco_de_custo=%s, preco_de_venda=%s WHERE idproduto=%s',
                (descricao,nosso,preco_de_custo,preco_de_venda,produto_id)
            )
        else:  # Se não houver idproduto, verificar se já existe e depois realizar INSERT
           cursor.execute('SELECT idproduto FROM produtos WHERE descricao = %s', (descricao,))
           existing_produto = cursor.fetchone()

           if existing_produto:
                return redirect(url_for('produtos.cadastro_produto', descricao=descricao))

           cursor.execute(
                'INSERT INTO produtos (descricao,nosso,preco_de_custo,preco_de_venda) VALUES (%s, %s, %s, %s)',
                (descricao,nosso,preco_de_custo,preco_de_venda)
           )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('produtos.cadastro_produto'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    descricao = request.args.get('descricao')
    produto = None

    if descricao:
        cursor.execute('SELECT * FROM produtos WHERE descricao = %s', (descricao,))
        produto = cursor.fetchone()

    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()

    produto_id = produto.get('idproduto') if produto else ''
    return render_template('cadastro_produto.html', produtos=produtos, produto=produto, produto_id=produto_id)

    #return render_template('cadastro_produto.html', produtos=produtos, produto=produto)


@bp.route('/excluir_produto/<int:idproduto>', methods=['GET'])
@login_required
def excluir_produto(idproduto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE idproduto = %s', (idproduto,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('produtos.cadastro_produto'))


@bp.route('/verificar_descricao', methods=['GET'])
@login_required
def verificar_descricao():
    descricao = request.args.get('descricao')
    print(descricao)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produtos WHERE descricao = %s', (descricao,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()

    if produto:
        return jsonify(produto)
    else:
        return jsonify(None)
