from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import get_db_connection

bp = Blueprint('entregas', __name__, url_prefix='/entregas')


@bp.route('/incluir', methods=['GET', 'POST'])
def incluir_entrega():

    conn = get_db_connection()
    conn.start_transaction()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Captura os dados do formulário
        numero_entrega = request.form['numero_entrega']
        data_entrega = request.form['data_entrega']
        idvenda = request.form['idvenda']
        idcaminhao = request.form['idcaminhao']
        quantidade = float(request.form['quantidade'])

        cursor.execute('''
            INSERT INTO entrega (numero_entrega, data_entrega, idvenda, idcaminhao, quantidade)
            VALUES (%s, %s, %s, %s, %s)
        ''', (numero_entrega, data_entrega, idvenda, idcaminhao, quantidade))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('entregas.incluir_entrega', teste='sim', msg='Entrega incluída com sucesso'))


    # Buscar vendas disponíveis
    cursor.execute("SELECT idvenda, numerovenda FROM vendas")  # Ajuste se necessário
    vendas = cursor.fetchall()

    # Buscar caminhões disponíveis
    cursor.execute("SELECT idcaminhao, CONCAT(placa, ' ', motorista) AS info_caminhao FROM caminhao")
    caminhoes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('incluir_entrega.html', vendas=vendas, caminhoes=caminhoes)


@bp.route('/verificar_entrega/<string:numero_entrega>', methods=['GET',  'POST'])
def verificar_entrega(numero_entrega):
    print("entrei no verificar entrega")
    print(numero_entrega)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM entrega WHERE numero_entrega = %s", (numero_entrega,))
    entrega_existente = cursor.fetchone()

    print('executei o sql')
    print(entrega_existente)

    # Trocar o formato da data de entrega, se necessário

    if entrega_existente is not None and 'data_entrega' in entrega_existente:
        entrega_existente['data_entrega'] = entrega_existente['data_entrega'].strftime('%Y-%m-%d')
    try:
       cursor.close()
       conn.close()
    except Exception as e:
        print(f"Ocorreu um erro de novo: {e}")

    print(entrega_existente)
    print('antes de fazer o return')

    if entrega_existente:
        print('vai true e o entrega_existente')
        return jsonify({"existe":True,"entrega":entrega_existente})
    else:
        print('vai false')
        return jsonify({"existe":False, "entrega": entrega_existente})




@bp.route('/excluir_entrega', methods=['POST'])
def excluir_entrega():
    numero_entrega = request.form['numeroentrega_excluir']
    retorno = verificar_entrega(numero_entrega)  # Essa função retorna um JSON
    resposta = retorno.json["existe"]

    if resposta:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entrega WHERE numero_entrega = %s", (numero_entrega,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('entregas.incluir_entrega', teste='sim', msg='Entrega excluída com sucesso'))
    else:
        return redirect(url_for('entregas.incluir_entrega', teste='sim', msg='Entrega não existia'))
