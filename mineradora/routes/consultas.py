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


@bp.route('/gerar_pdf_cliente', methods=['POST'])
def gerar_pdf_cliente():
    global clientes_global
    if not clientes_global:
        return "Nenhum cliente encontrado.", 404

    # Obtém o formato selecionado pelo usuário (ficha ou lista)
    formato = request.form.get('formato', 'ficha')

    # Criação do PDF
    pdf = FPDF()

    # Ajusta a orientação manualmente para landscape apenas no formato lista
    if formato == 'lista':
        pdf.add_page(orientation='L')  # Define para landscape
    else:
        pdf.add_page()  # Padrão é retrato

    # Adiciona o logo no topo centralizado

    logo_path = 'static/images/logopequeno.jpg'
    # Obtém a largura da página e a largura da imagem
    page_width = pdf.w
    logo_width = 20  # Você pode ajustar a largura do logo conforme necessário
    logo_x = (page_width - logo_width) / 2  # Centraliza a imagem

    # Adiciona a imagem, a posição X e Y e a largura
    pdf.image(logo_path, x=logo_x, y=10, w=logo_width)

    # Adiciona um título centralizado abaixo do logo
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt="Consulta de Cliente", ln=True, align="L")
    pdf.ln(10)

    if formato == 'ficha':
        # Formato Ficha: exibe os dados de cada cliente em blocos
        for cliente in clientes_global:
            for campo, valor in cliente.items():
                linha = f"{campo.capitalize()}: {valor}"
                pdf.cell(0, 10, txt=linha, ln=True)
            pdf.ln(10)
    elif formato == 'lista':
        # Larguras específicas para cada coluna
        col_widths = {
            "cnpj_cpf": 30,
            "razao_social": 40,
            "apelido": 30,
            "telefones": 45,
            "email": 50,
            "endereco": 70,
            "distancia_km": 20
        }

        pdf.set_font("Arial", "B", 12)
        headers = ["CNPJ - CPF", "Razão Social", "Apelido", "Telefones", "Email", "Endereço", "Dist.km"]
        for i, header in enumerate(headers):
            pdf.cell(col_widths[list(col_widths.keys())[i]], 10, header, border=1, align="C")
        pdf.ln()

        # Conteúdo da tabela
        pdf.set_font("Arial", size=10)
        for cliente in clientes_global:
            pdf.cell(col_widths["cnpj_cpf"], 10, str(cliente.get("cnpj_cpf", "")), border=1, align="C")
            pdf.cell(col_widths["razao_social"], 10, cliente.get("razao_social", ""), border=1)
            pdf.cell(col_widths["apelido"], 10, cliente.get("apelido", ""), border=1)
            pdf.cell(col_widths["telefones"], 10, cliente.get("telefones", ""), border=1)
            pdf.cell(col_widths["email"], 10, cliente.get("email", ""), border=1)
            pdf.cell(col_widths["endereco"], 10, cliente.get("endereco", ""), border=1)
            pdf.cell(col_widths["distancia_km"], 10, str(cliente.get("distancia_km", "")), border=1, align="C")
            pdf.ln()

    # Geração do PDF para download
    pdf_output = pdf.output(dest='S').encode('latin1')
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=consulta_cliente.pdf'

    return response

@bp.route('/consultavenda', methods=['GET', 'POST'])
def consulta_vendas():
    vendas = []
    if request.method == 'POST':
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        # Conexão com o banco de dados
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            v.numerovenda, 
            v.data_venda, 
            c.apelido AS cliente, 
            p.descricao AS produto, 
            v.valor_produto AS "preco_de_tabela",
            v.valor_produto_negociado AS "valor_vendido",
            v.quantidade,
            v.valor_frete,
            (v.valor_produto_negociado * v.quantidade + v.valor_frete) AS total
        FROM 
            vendas v
        JOIN 
            clientes c ON v.idcliente = c.idcliente
        JOIN 
            produtos p ON v.idproduto = p.idproduto
        WHERE 
            v.data_venda BETWEEN %s AND %s
        ORDER BY 
            v.data_venda, p.descricao
        """

        cursor.execute(query, (data_inicio, data_fim))
        vendas = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('consultavenda.html', vendas=vendas)
