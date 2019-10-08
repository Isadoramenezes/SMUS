import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE umidade (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        umidade TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW
    );
    CREATE TABLE login (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")

print('Tabela umidade criada com sucesso.')

conn.close()
