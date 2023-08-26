# Importa bibliotecas 
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime

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
def load_user(user_id):
    return User.query.get(int(user_id))

# Classe User (tabela de usuários do BD SQLite)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    cpf = db.Column(db.Integer, nullable = True, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    dt_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    cep = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return '<ID %r>' % self.id

# Classes de formulários (flask_forms e wtforms)
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

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Digite seu e-mail..."})
    senha = PasswordField('Senha', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Digite sua senha..."})
    submit = SubmitField('Entrar')

# Roteamento do flask (direciona para as devidas páginas html)
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
                login_user(user)
                return redirect(url_for('pesquisa'))
            
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
        novo_usuario = User(nome=form.nome.data, email=form.email.data, cpf=form.cpf.data, senha=hash_senha, cep=form.cep.data)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('cadastro.html', form=form)

@app.route('/pesquisa', methods=['POST','GET'])
@login_required
def pesquisa():
    userid = current_user.get_id()
    user = User.query.filter_by(id=userid).first()
    username = user.nome
    nomecompleto = username.split()
    nome = nomecompleto[0]
    return render_template('pesquisa.html', nome=nome)

if __name__ == "__main__":
    app.run(debug=True)