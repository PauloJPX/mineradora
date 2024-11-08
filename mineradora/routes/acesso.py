from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_db_connection



bp = Blueprint('acesso', __name__, url_prefix='/acesso')


# Rota para exibir o formulário de cadastro de acessos
@bp.route('/cadastro_acesso', methods=['GET', 'POST'])
def cadastro_acesso():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obter todos os usuários
    cursor.execute("SELECT idusuario, usuario FROM usuarios")
    usuarios = cursor.fetchall()

    # Obter todos os módulos
    cursor.execute("SELECT idmodulo, nome_modulo FROM modulo")
    modulos = cursor.fetchall()

    modulos_selecionados = []

    # Se o método for GET (quando estamos carregando a página de cadastro)
    if request.method == 'GET':
        usuario_id = request.args.get('usuario', type=int)
        print (usuario_id)
        if usuario_id:
            # Buscar módulos já atribuídos ao usuário
            cursor.execute("""
                SELECT idmodulo FROM acesso WHERE idusuario = %s
            """, (usuario_id,))
            modulos_selecionados = [modulo['idmodulo'] for modulo in cursor.fetchall()]
            print(modulos_selecionados)
            print("=======================")
    # Se o método for POST (quando estamos salvando os acessos)
    if request.method == 'POST':
        idusuario = request.form.get('usuario')
        modulos_selecionados = request.form.getlist('modulos')

        # Apagar os acessos existentes do usuário
        cursor.execute("DELETE FROM acesso WHERE idusuario = %s", (idusuario,))

        # Inserir os novos acessos
        for idmodulo in modulos_selecionados:
            cursor.execute(
                "INSERT INTO acesso (idusuario, idmodulo) VALUES (%s, %s)",
                (idusuario, idmodulo)
            )

        conn.commit()
        flash('Acessos atualizados com sucesso!')
       # return redirect(url_for('menu.menu_principal'))
        redirect_url = url_for('menu.menu_principal')
        return f"""
        <script>
            window.top.location.href = '{redirect_url}';
        </script>
        """

    cursor.close()
    conn.close()

    return render_template('cadastro_acesso.html', usuarios=usuarios, modulos=modulos,
                           modulos_selecionados=modulos_selecionados)
