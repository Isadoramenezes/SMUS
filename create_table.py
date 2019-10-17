import sqlite3

print(" ")
print("........ FAZENDO CONEXÃO COM O BANCO ........")
print(" ")
conn = sqlite3.connect('static/database.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS umidade (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        umidade TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW
    );
""")

print('.......Tabela umidade criada com sucesso..........')
print(" ")
print(".......... CRIANDO TABELA USUARIOS ..........")
print(" ")

cursor.execute("""
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
  );
""")
conn.commit()

print(" ")
print("............. INSERINDO ADMIN ...............")
print(" ")

cursor.execute("""
  INSERT INTO users (id, username, password) 
  VALUES (NULL, 'admin', 'admin')
""")
conn.commit()
cursor.execute("""
  INSERT INTO users (id, username, password) 
  VALUES (NULL, 'teste', '1234')
""")

conn.commit()
conn.close()
