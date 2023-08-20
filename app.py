# Importa bibliotecas 
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instancia o Flask e configura o banco de dados SQLite
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bdwebapp.db"
db = SQLAlchemy()
db.init_app(app)

# Classe Usuarios (tabela do BD SQLite)
class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.Integer, nullable = True)
    senha = db.Column(db.String(30), nullable=False)
    dt_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    cep = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return '<Task %r>' % self.id

# Aciona a página (URL) index.html
@app.route('/', methods=['POST','GET'])
@app.route('/index.html', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

@app.route('/pesquisa.html')
def pesquisa():
    return render_template('pesquisa.html')

if __name__ == "__main__":
    app.run(debug=True)