# cadastro de caminhoes
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import get_db_connection
from req import login_required,pode

bp = Blueprint('caminhoes', __name__, url_prefix='/caminhoes')


@bp.route('/cadastro_caminhao', methods=['GET', 'POST'])
@login_required
@pode('Caminhões')
def cadastro_caminhao():
    if request.method == 'POST':
        placa = request.form['placa']
        modelo = request.form['modelo']
        ano = request.form['ano']
        capacidade = request.form['capacidade']
        proprietario = request.form['proprietario']
        motorista = request.form['motorista']
        capacidade_tanque = request.form['capacidade_tanque']
        caminhao_id = request.form.get('idcaminhao')  # Alterado para idcaminhao

        if capacidade:
            try:
                capacidade = float(capacidade)
            except ValueError:
                return "Erro: O campo 'capacidade' deve ser um número.", 400

        if capacidade_tanque:
            try:
                capacidade_tanque = float(capacidade_tanque)
            except ValueError:
                return "Erro: O campo 'capacidade do tanque' deve ser um número.", 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if caminhao_id:  # Se idcaminhao estiver presente, realizar UPDATE
            cursor.execute(
                'UPDATE caminhao SET placa=%s, modelo=%s, ano=%s, capacidade=%s, proprietario=%s, motorista=%s, capacidade_tanque=%s WHERE idcaminhao=%s',
                (placa, modelo, ano, capacidade, proprietario, motorista, capacidade_tanque, caminhao_id)
            )
        else:  # Se não houver idcaminhao, verificar se já existe e depois realizar INSERT
            cursor.execute('SELECT idcaminhao FROM caminhao WHERE placa = %s', (placa,))
            existing_caminhao = cursor.fetchone()

            if existing_caminhao:
                return redirect(url_for('caminhoes.cadastro_caminhao', placa=placa))

            cursor.execute(
                'INSERT INTO caminhao (placa, modelo, ano, capacidade, proprietario, motorista, capacidade_tanque) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (placa, modelo, ano, capacidade, proprietario, motorista, capacidade_tanque)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('caminhoes.cadastro_caminhao'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    placa = request.args.get('placa')
    caminhao = None

    if placa:
        cursor.execute('SELECT * FROM caminhao WHERE placa = %s', (placa,))
        caminhao = cursor.fetchone()

    cursor.execute('SELECT * FROM caminhao')
    caminhões = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('cadastro_caminhao.html', caminhões=caminhões, caminhao=caminhao)


@bp.route('/excluir_caminhao/<int:idcaminhao>', methods=['GET'])
def excluir_caminhao(idcaminhao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM caminhao WHERE idcaminhao = %s', (idcaminhao,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('caminhoes.cadastro_caminhao'))




@bp.route('/verificar_placa', methods=['GET'])
def verificar_placa():
    placa = request.args.get('placa')

    # Usar a função para obter a conexão
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM caminhao WHERE placa = %s", (placa,))
        caminhao = cursor.fetchone()

    # Fechar a conexão após o uso
    conn.close()

    if caminhao:
        print(f"Caminhão encontrado: {caminhao}")  # Log do caminhão encontrado
        return jsonify({
            'idcaminhao': caminhao[0],
            'modelo': caminhao[1],
            'ano': caminhao[3],
            'capacidade': caminhao[4],
            'proprietario': caminhao[5],
            'motorista': caminhao[6],
            'capacidade_tanque': caminhao[7]
        })
    else:
        print("Caminhão não encontrado")  # Log quando não encontrar
        return jsonify(None)
