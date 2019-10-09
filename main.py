import sqlite3
from flask import Flask, render_template
from create_table import conn



debug = True
app   = Flask(__name__)

# funcao responsavel por efetuar a leitura do banco de dados e nos retornar as temperaturas cadastradas
def getUmidade():
    conn   = sqlite3.connect('database.db')
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