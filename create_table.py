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
    username TEXT NOT NULL,
    password TEXT NOT NULL
  );
""")
conn.commit()
print(" ")
print("........... Tabela de Usuários criadaS ...........")
print(" ")


cursor.execute("""
  INSERT INTO users (id, username, password) 
  VALUES (NULL, 'admin', 'admin')
""")
conn.commit()
print(" ")
print("................. ADMIN Inserido .................")
print(" ")
conn.close()
