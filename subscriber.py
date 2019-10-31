import urllib.request
import json
import sqlite3
import functools
import operator

alerta = input("Defina um Alerta: ")
alerta = int(alerta)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def verificaNivel(alerta):
      cursor.execute("""
        SELECT field1 FROM umidade
        WHERE entry_id = (SELECT MAX(entry_id) FROM umidade)
      """)
      nivelAtual = cursor.fetchall()
      listaAtual = nivelAtual[0]
      nivelInteiro = functools.reduce(operator.add, (listaAtual))
      if nivelInteiro > alerta:
        print("O NÍVEL ATINGIU ", nivelInteiro)
      return nivelInteiro

while True:
  TS = urllib.request.urlopen("https://api.thingspeak.com/channels/879252/fields/1.json?results=1")
  response = TS.read()
  data=json.loads(response)
  newList = data['feeds']
  for x in newList:
    columns = ', '.join(x.keys())
    placeholders = '"'+'", "'.join(map(str, x.values()))+'"'
    query = 'INSERT INTO umidade (%s) VALUES (%s)' % (columns, placeholders)
    print(query)
    cursor.execute(query)
    conn.commit()   
    verificaNivel(alerta)
  break
conn.close()
TS.close()

