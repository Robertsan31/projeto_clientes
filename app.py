from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Inicializa o app antes de configurar o banco!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Agora o banco pode ser inicializado!

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template("cadastro.html")

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    
    novo_cliente = Cliente(nome=nome, cpf=cpf, email=email)
    db.session.add(novo_cliente)
    db.session.commit()

    return f"Cadastro realizado com sucesso! Nome: {nome}, CPF: {cpf}, Email: {email}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

