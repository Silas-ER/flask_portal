from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from models import User, Setores
from sqlalchemy import text
import pyodbc, os
from flask_bcrypt import Bcrypt
from services.api_news import news
from services.what_suport import enviar_mensagem
from services.birthday import aniversariantes
from dotenv import load_dotenv

load_dotenv()

lista_de_setores = ['RH', 'Almoxarifado', 'Escritório', 'Financeiro', 'Frota', 'Loja', 'Operacional']

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.getenv('SECRET_KEY') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')  
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/')
def home():
    news_data = news()
    aniversariantes_lista = aniversariantes()
    return render_template('home.html', news=news_data, aniversariantes_lista=aniversariantes_lista)

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/suporte', methods=['GET', 'POST'])
def suporte():    
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        email = request.form['email'].strip() 
        telefone = request.form['telefone'].strip()
        tipo = request.form['tipo'].strip()       
        setor = request.form['setor'].strip()
        problema = request.form['problema'].strip()

        try:
            enviar_mensagem(usuario, telefone, email,tipo, setor, problema)
            flash('Solicitação enviada!')
        except Exception as e:
            flash('Erro de solicitação!')

    return render_template('suporte.html', lista_de_setores=lista_de_setores)

@app.route('/solicitar')
def solicitar():
    pass

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip() 

        try:
            with db.session.begin():
                sql_file_path = os.path.join(os.path.dirname(__file__), 'login.sql')
                with open(sql_file_path, 'r') as f:
                    query = f.read()

                result = db.session.execute(text(query), {'USERNAME': username, 'PASSWORD': password}).fetchone()

                if result and result[1] == password:  # Compara a senha em texto plano
                    user = User(result[0], result[1], result[2])  # Cria o objeto User com os valores da tupla
                    return redirect(url_for('suporte'))
                else:
                    flash('Usuário ou senha incorretos!')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro durante o login: {e}')

    return render_template('login.html')

app.run(host='0.0.0.0', port=8080, debug=True)