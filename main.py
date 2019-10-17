import sqlite3
from flask import Flask, render_template, redirect, url_for, request, g
import create_table
from create_table import conn

debug = True
app   = Flask(__name__)
##############################################################
############### VALIDATE LOGIN FUNCTION ######################
##############################################################
def validate(username, password):
    conn = sqlite3.connect('static/database.db')
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
##############################################################
################### CHAMADAS DE LOGIN ########################
##############################################################    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

@app.route('/secret')
def secret():
    return "Você está logado!"
    
# funcao responsavel por efetuar a leitura do banco de dados e nos retornar as temperaturas cadastradas
def getUmidade():
    conn   = sqlite3.connect('static/database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, umidade, strftime('%d/%m/%Y %H:%M:%S', created_at) as created_at FROM umidade
        ORDER BY id DESC
        LIMIT 50;
    """)

    return cursor.fetchall()

    conn.close()

@app.route('/')

def index():
    return render_template('index.html', umidades=getUmidade())

if __name__ == "__main__":
    if debug:
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=8080)