import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#Criar verificação de existência da tabela
cursor.execute("""
    CREATE TABLE IF NOT EXISTS umidade (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        umidade TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW
    );
""")

print('Tabela umidade criada com sucesso.')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
    );
""")
print("tabela de usuário criada com sucesso")

cursor.execute("""
    INSERT INTO usuarios VALUES(1, 'admin@admin.com', '1234')
""")
print("Usuário admin criado com sucesso")

conn.close()
