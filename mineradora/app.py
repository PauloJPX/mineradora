from flask import Flask, session, redirect, url_for
from config import Config
from functools import wraps
from routes import auth, usuarios, menu, clientes
from routes import vendas  # Adicione vendas aqui

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth.bp)
app.register_blueprint(usuarios.bp)
app.register_blueprint(clientes.bp)
app.register_blueprint(menu.bp)
app.register_blueprint(vendas.bp)  # Registra o blueprint de vendas

@app.route('/')
@login_required
def home():
    return redirect(url_for('menu.menu_principal'))

if __name__ == '__main__':
    app.run(debug=True)
