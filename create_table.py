import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print(" ")
print(".................. BANCO CRIADO ...................")
print(" ")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS umidade (
        entry_id INTEGER NOT NULL,
        created_at BLOB NOT NULL,
        field1 INTEGER NOT NULL
    );
""")
print('...............Tabela Umidade criada ..............')
cursor.execute("""
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
  );
""")
conn.commit()
print(" ")
print("........... Tabela de Usuários criada .............")
print(" ")
conn.close()