from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/login')
def login():
    return render_template('login.html')

app.run(host='0.0.0.0', port=8080, debug=True)