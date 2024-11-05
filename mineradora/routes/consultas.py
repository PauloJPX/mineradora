# consultas.py
from flask import Blueprint, render_template, request
from models import get_db_connection  # Importa a função de conexão

from fpdf import FPDF
from flask import make_response

clientes_global= []

bp = Blueprint('consultas', __name__, url_prefix='/consultas')

@bp.route('/', methods=['GET'])
def pagina_consultas():
    return render_template('consultas.html')  # Certifique-se de que a página 'consultas.html' existe

@bp.route('/consultacliente', methods=['GET'])
def consulta_cliente():
    global clientes_global  # Acessa a variável global
    # Conecta ao banco de dados usando a função de models.py
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtém o filtro da Razão Social, se houver
    razao_social = request.args.get('razao_social')
    if razao_social:
        query = "SELECT * FROM clientes WHERE razao_social LIKE %s"
        cursor.execute(query, ('%' + razao_social + '%',))
    else:
        query = "SELECT * FROM clientes"
        cursor.execute(query)

    # Recupera os dados dos clientes
    clientes = cursor.fetchall()
    clientes_global = clientes
    print(clientes_global)
    cursor.close()
    conn.close()

    return render_template('consultacliente.html', clientes=clientes, razao_social=razao_social)


@bp.route('/gerar_pdf_cliente', methods=['GET', 'POST'])
def gerar_pdf_cliente():
    global clientes_global  # Acessa a variável global
    print("Geração de PDF iniciada")  # Linha para depuração
    print('vou imprimir o cliente_global')
    print(clientes_global)
    # Verifica se há dados de clientes disponíveis
    if not clientes_global:
        return "Nenhum cliente encontrado.", 404  # Retorna erro se não houver clientes

    # Simulação dos dados do cliente
    dados_cliente = {
        'nome': 'João da Silva',
        'cpf': '123.456.789-00',
        'email': 'joao@example.com',
        'telefone': '(11) 99999-9999',
        'endereco': 'Rua Exemplo, 123, Bairro Centro, São Paulo, SP'
    }

    # Criação do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adicionando conteúdo ao PDF
    pdf.cell(200, 10, txt="Consulta de Cliente", ln=True, align="C")
    pdf.ln(10)  # Adiciona uma linha em branco

    print(clientes_global)

    #for campo, valor in dados_cliente.items():
    #    linha = f"{campo.capitalize()}: {valor}"  # Formata a linha
    #    print(linha)
    #    pdf.cell(200, 10, txt=linha, ln=True)  # Adiciona a linha ao PDF

    # Adicionando os dados de todos os clientes
    for cliente in clientes_global:
        for campo, valor in cliente.items():
            linha = f"{campo.capitalize()}: {valor}"  # Formata a linha
            print(linha)
            pdf.cell(200, 10, txt=linha, ln=True)  # Adiciona a linha ao PDF

    # Geração do PDF para download
    pdf_output = pdf.output(dest='S').encode('latin1')  # Certifique-se de gerar como bytes
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=consulta_cliente.pdf'

    return response

# Você pode adicionar outras rotas relacionadas a consultas aqui, se necessário.
