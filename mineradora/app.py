from flask import Flask, session, redirect, url_for, request
from config import Config
from functools import wraps
from routes import auth, usuarios, menu, clientes, vendas, inicio,  caminhoes

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.config.from_object(Config)

# Registrar os blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(usuarios.bp)
app.register_blueprint(clientes.bp)
app.register_blueprint(menu.bp)
app.register_blueprint(vendas.bp)
app.register_blueprint(inicio.bp)
app.register_blueprint(caminhoes.bp)

# Proteger todas as rotas do blueprint de vendas
@app.before_request
def require_login():

    listaMenu= ['vendas.', 'usuarios.', 'menu.', 'clientes.', 'caminhoes.']

    for menu in listaMenu:
        if request.endpoint and request.endpoint.startswith(menu) and 'logged_in' not in session:
            return redirect(url_for('auth.login'))


@app.route('/')
@login_required
def home():
    return redirect(url_for('menu.menu_principal'))

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
