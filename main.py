import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, PasswordField, validators, IntegerField
import create_table
from subscriber import subscriber

debug = True
app   = Flask(__name__)

class RegisterForm(Form):
  acesso = StringField('Tipo de Usuario', [validators.Length(min = 0, max = 1, message='escolha 0 para admin e 1 para morador')])
  name = StringField('Nome', [validators.Length(min=1, max=50)])
  username = StringField('Nome de usuario', [validators.Length(min=4, max=25)])
  email = StringField('Email', [validators.Length(min=6, max=50)])
  password = PasswordField('Senha', [
      validators.DataRequired(),
      validators.EqualTo('confirm', message='Senhas não coincidem. Tente novamente')
  ])
  confirm = PasswordField('Confirmação de Senha')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm(request.form)
  if request.method == 'POST' and form.validate():
    acesso = form.acesso.data
    name = form.name.data
    email = form.email.data
    username = form.username.data
    password = (form.password.data)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = "INSERT INTO users(name, email, username, password, acesso) VALUES(?, ?, ?, ?, ?);"
    cursor.execute(sql, (str(name), str(email), str(username), str(password), acesso))
    conn.commit()
    cursor.close()
    
    flash('Registro feito!', 'sucesso')
    return redirect(url_for('login'))
  return render_template('register.html', form=form)

class Alerta(Form):
  nivelAlerta = IntegerField('Novo Alerta', [validators.required(message='Escolha um valor entre 0 e 100')])

@app.route('/alertManager', methods = ['GET', 'POST'])
def alertManager():
  form = Alerta(request.form)
  novoAlerta = Alerta()
  if request.method == 'POST' and form.validate():
    novoAlerta = form.nivelAlerta.data
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql_alerta ='INSERT INTO controle_de_nivel (nivel_alerta) VALUES (%s)' % (novoAlerta)
    print("SQL ALERTA")
    print(sql_alerta)
    cursor.execute(sql_alerta)
    conn.commit()
    cursor.close
    return redirect(url_for('alertManager'))
  return render_template('alertManager.html', form=novoAlerta)

def validate(username, password):
  conn = sqlite3.connect('database.db')
  completion = False
  with conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
      dbUser = row[1]
      dbPass = row[4]
      if dbUser==username and dbPass == password:
        completion=(dbPass, password)
  return completion

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    completion = validate(username, password)
    if completion == False:
      error = 'Usuário ou senha inválidos. Por favor, tente novamente.'
    else:
      conn = sqlite3.connect('database.db')
      with conn:
        print("entrou no with")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ('%s') " %  username)
        rows = cursor.fetchall()
        for row in rows:
          userdb = row[1]
          userpass = row[4]
          acesso = row[5]
          if acesso == 0 and userdb == username and userpass == password:
            return redirect(url_for('alertManager'))
          else:
            return redirect(url_for('secret'))
  return render_template('login.html')

@app.route('/secret')
def secret():
  return "Você está logado!"

def getUmidade():
  conn   = sqlite3.connect('database.db',)
  cursor = conn.cursor()

  cursor.execute("""
      SELECT entry_id, field1, created_at FROM umidade
      ORDER BY entry_id DESC
      LIMIT 10;
  """)
  return cursor.fetchall()
  conn.close()

@app.route('/')
def index():
  sinalAlerta = subscriber()
  return render_template('index.html', umidade=getUmidade(), atualizacao = subscriber(), status = sinalAlerta)

if __name__ == "__main__":
  app.secret_key = 'super secret key'
  if debug:
      app.run(host='0.0.0.0', port=8080, debug=True)
  else:
      app.run(host='0.0.0.0', port=8080)