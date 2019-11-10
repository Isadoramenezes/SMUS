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

cursor.execute("""
  INSERT INTO umidade(entry_id, created_at, field1) VALUES (0, '2019-11-02T23:09:54Z', 0)
""")
print('...............Tabela Umidade criada ..............')
cursor.execute("""
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    acesso INT NOT NULL
  );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS controle_de_nivel (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nivel_alerta INTEGER NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

cursor.execute("""
  INSERT INTO controle_de_nivel(nivel_alerta) VALUES (100)
""")

conn.commit()
print(" ")
print("........... Tabela de Usuários criada .............")
print(" ")
conn.close()