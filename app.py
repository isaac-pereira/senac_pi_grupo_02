# Importa bibliotecas 
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, DateField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime
import json

# Instancia o Flask e realiza as configurações gerais (banco de dados, criptografia, gerenciador de login)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bdwebapp.db"
app.config['SECRET_KEY'] = '123abc_secret_key_cba321'
db = SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

## Banco de dados e tabelas

# Classe Carrinho
class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quantidade = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('produto.id'))     

# Classe Produtos (tabela de produtos)
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome_produto = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    vencimento = db.Column(db.DateTime, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    lojista_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Classe User (tabela de usuários do BD SQLite)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    cpf = db.Column(db.Integer, nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    dt_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    cep = db.Column(db.Integer, nullable = False)
    tipo_user = db.Column(db.Integer, nullable = False)
    prod_lojista = db.relationship('Produto', backref='lojista')
    prod_carrinho = db.relationship('Carrinho', backref='cliente')

    def __repr__(self):
        return '<ID %r>' % self.id

# Cria o banco de dados e as tabelas, caso não existam no diretório 'instance' do aplicativo
with app.app_context():
    db.create_all()

## Classes de formulários (flask_forms e wtforms)

# Cadastro Cliente/Consumidor (registro ou Sign-up)
class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Digite seu nome..."})
    email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Digite seu e-mail..."})
    cpf = IntegerField('CPF', validators=[InputRequired()], render_kw={"placeholder": "Digite seu CPF..."})
    senha = PasswordField('Senha', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Digite sua senha..."})
    cep = IntegerField('CEP', validators=[InputRequired()], render_kw={"placeholder": "Digite seu CEP..."})
    submit = SubmitField('Enviar')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('E-mail de usuário já cadastrado.')
    
    def validate_cpf(self, cpf):
        existing_user_cpf = User.query.filter_by(cpf=cpf.data).first()
        if existing_user_cpf:
            raise ValidationError('CPF de usuário já cadastrado.')
        
# Cadastro Lojista (registro ou Sign-up)
class RegisterFormPJ(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Digite o nome do Mercado..."})
    email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Digite seu e-mail..."})
    cpf = IntegerField('CNPJ', validators=[InputRequired()], render_kw={"placeholder": "Digite o CNPJ..."})
    senha = PasswordField('Senha', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Digite sua senha..."})
    cep = IntegerField('CEP', validators=[InputRequired()], render_kw={"placeholder": "Digite o CEP..."})
    submit = SubmitField('Enviar')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('E-mail de usuário já cadastrado.')
    
    def validate_cpf(self, cpf):
        existing_user_cpf = User.query.filter_by(cpf=cpf.data).first()
        if existing_user_cpf:
            raise ValidationError('CPF de usuário já cadastrado.')

# Login
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Digite seu e-mail..."})
    senha = PasswordField('Senha', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Digite sua senha..."})
    submit = SubmitField('Entrar')

# Adiciona Produto no Estoque - Lojista
class ProductForm(FlaskForm):
    nome_produto = StringField('Nome do Produto', validators=[InputRequired(), Length(min=1, max=150)], render_kw={"placeholder": "Digite o nome do produto..."})
    preco = DecimalField('Preço', places=2, validators=[InputRequired()], render_kw={"placeholder": "Digite o preço do produto..."})
    vencimento = DateField('Vencimento do Anúncio', format='%Y-%m-%d',  render_kw={"placeholder": "Digite o vencimento da oferta..."})
    quantidade = IntegerField('Quantidade', validators=[InputRequired()], render_kw={"placeholder": "Digite a quantidade disponível..."})
    submit = SubmitField('Confirmar')

# Adiciona Produto no Carrinho/Lista de Compras - Cliente/Consumidor
class IncluiNoCarrinho(FlaskForm):
    product_id = IntegerField()
    submit = SubmitField('Incluir na lista')

## Roteamento do flask (direciona para as devidas páginas html)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, form.senha.data):
                login_user(user, remember=True)
                if user.tipo_user == 0:
                    return redirect(url_for('pesquisa', user=current_user))
                else:
                    return redirect(url_for('estoque', user=current_user))
            else:
                flash('E-mail e/ou senha incorretos!')
                return redirect(url_for('login'))
        else:
            flash('E-mail e/ou senha incorretos!')
            return redirect(url_for('login'))
            
    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['POST','GET'])
def cadastro():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_senha = bcrypt.generate_password_hash(form.senha.data)
        novo_usuario = User(nome=form.nome.data, email=form.email.data, cpf=form.cpf.data, senha=hash_senha, cep=form.cep.data, tipo_user=0)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('cadastro.html', form=form)

@app.route('/cadastro_pj', methods=['POST','GET'])
def cadastro_pj():
    form = RegisterFormPJ()

    if form.validate_on_submit():
        hash_senha = bcrypt.generate_password_hash(form.senha.data)
        novo_usuario = User(nome=form.nome.data, email=form.email.data, cpf=form.cpf.data, senha=hash_senha, cep=form.cep.data, tipo_user=1)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('cadastro_pj.html', form=form)

@app.route('/pesquisa', methods=['POST','GET'])
@login_required
def pesquisa():
    user_id = int(current_user.get_id())
    user = User.query.filter_by(id=user_id).first()
    username = user.nome
    nomecompleto = username.split()
    nome = nomecompleto[0]

    prod_disponiveis = Produto.query.order_by(Produto.nome_produto).all()

    form_inclui = IncluiNoCarrinho()

    if form_inclui.validate_on_submit():
        novo_carrinho = Carrinho(product_id=form_inclui.product_id.data, user_id=current_user.id)
        db.session.add(novo_carrinho)
        db.session.commit()
        flash('Produto incluído no carrinho com sucesso!')

    return render_template('pesquisa.html', user=current_user, nome=nome, prod_disponiveis=prod_disponiveis, form_inclui=form_inclui)

@app.route('/estoque', methods=['POST','GET'])
@login_required
def estoque():
    user_id = int(current_user.get_id())
    user = User.query.filter_by(id=user_id).first()
    username = user.nome
    nomecompleto = username.split()
    nome = nomecompleto[0]

    return render_template('EstoqueVirtual.html', user=current_user, nome=nome)

@app.route('/adiciona_produto', methods=['POST','GET'])
@login_required
def adiciona_produto():
    
    user_id = int(current_user.get_id())
    user = User.query.filter_by(id=user_id).first()
    username = user.nome
    nomecompleto = username.split()
    nome = nomecompleto[0]

    form = ProductForm()

    if form.validate_on_submit():
        novo_produto = Produto(nome_produto=form.nome_produto.data, preco=form.preco.data, vencimento=form.vencimento.data, quantidade=form.quantidade.data, lojista_id=current_user.id)
        db.session.add(novo_produto)
        db.session.commit()
    return render_template('AdicionarProduto.html', user=current_user, nome=nome, form=form)

@app.route('/delete-produto', methods=['POST'])
def delete_produto():  
    produto = json.loads(request.data)
    produtoId = produto['produtoId']
    produto = Produto.query.get(produtoId)
    if produto:
        if produto.lojista_id == current_user.id:
            db.session.delete(produto)
            db.session.commit()

    return jsonify({})

## Inicializa a aplicação
if __name__ == "__main__":
    app.run(debug=True)