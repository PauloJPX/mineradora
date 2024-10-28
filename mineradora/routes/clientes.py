from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import get_db_connection

bp = Blueprint('clientes', __name__, url_prefix='/clientes')


@bp.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        cnpj_cpf = request.form['cnpj_cpf']
        razao_social = request.form['razao_social']
        apelido = request.form['apelido']
        telefones = request.form['telefones']
        email = request.form['email']
        endereco = request.form['endereco']
        distancia_km = request.form['distancia']
        cliente_id = request.form.get('idcliente')  # Alterado para idcliente

        if distancia_km:
            try:
                distancia_km = float(distancia_km)
            except ValueError:
                return "Erro: O campo 'distância em km' deve ser um número.", 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if cliente_id:  # Se idcliente estiver presente, realizar UPDATE
            cursor.execute(
                'UPDATE clientes SET cnpj_cpf=%s, razao_social=%s, apelido=%s, telefones=%s, email=%s, endereco=%s, distancia_km=%s WHERE idcliente=%s',
                (cnpj_cpf, razao_social, apelido, telefones, email, endereco, distancia_km, cliente_id)
            )
        else:  # Se não houver idcliente, verificar se já existe e depois realizar INSERT
            cursor.execute('SELECT idcliente FROM clientes WHERE cnpj_cpf = %s', (cnpj_cpf,))
            existing_client = cursor.fetchone()

            if existing_client:
                return redirect(url_for('clientes.cadastro_cliente', cnpj_cpf=cnpj_cpf))

            cursor.execute(
                'INSERT INTO clientes (cnpj_cpf, razao_social, apelido, telefones, email, endereco, distancia_km) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (cnpj_cpf, razao_social, apelido, telefones, email, endereco, distancia_km)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('clientes.cadastro_cliente'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cnpj_cpf = request.args.get('cnpj_cpf')
    cliente = None

    if cnpj_cpf:
        cursor.execute('SELECT * FROM clientes WHERE cnpj_cpf = %s', (cnpj_cpf,))
        cliente = cursor.fetchone()

    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('cadastro_cliente.html', clientes=clientes, cliente=cliente)


@bp.route('/excluir_cliente/<int:idcliente>', methods=['GET'])
def excluir_cliente(idcliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE idcliente = %s', (idcliente,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('clientes.cadastro_cliente'))


@bp.route('/verificar_cnpj', methods=['GET'])
def verificar_cnpj():
    cnpj_cpf = request.args.get('cnpj_cpf')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes WHERE cnpj_cpf = %s', (cnpj_cpf,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        return jsonify(cliente)
    else:
        return jsonify(None)
