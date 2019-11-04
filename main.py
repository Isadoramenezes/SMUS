import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import create_table
import subscriber


debug = True
app   = Flask(__name__)

class RegisterForm(Form):
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
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = (form.password.data)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        sql = "INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?);"
        cursor.execute(sql, (str(name), str(email), str(username), str(password)))
        conn.commit()
        cursor.close()
        flash('Registro feito!', 'sucesso')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

def validate(username, password):
    conn = sqlite3.connect('database.db')
    completion = False
    with conn:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM users")
      rows = cursor.fetchall()
      for row in rows:
          dbUser = row[1]
          dbPass = row[2]
          if dbUser==username:
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
            return redirect(url_for('secret'))
    return render_template('login.html')

@app.route('/secret')
def secret():
    return "Você está logado!"

@app.route('/base')
def base():
  return render_template('base.html')

def getUmidade():
    conn   = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT entry_id, field1, created_at FROM umidade
        ORDER BY entry_id DESC
        LIMIT 50;
    """)
    return cursor.fetchall()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html', umidade=getUmidade())

if __name__ == "__main__":
    app.secret_key = 'super secret key'
  
    if debug:
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=8080)