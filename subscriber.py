import urllib.request
import json
import sqlite3
import functools
import operator

alerta = 0

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

select = cursor.execute("SELECT entry_id FROM umidade WHERE entry_id = (SELECT MAX(entry_id) FROM umidade)")
idAtual = cursor.fetchall()
leituraAtual = idAtual[0]
ultimoID = functools.reduce(operator.add, (leituraAtual))
print(ultimoID)

while True:
  TS = urllib.request.urlopen("https://api.thingspeak.com/channels/879252/fields/1.json?results=10")
  response = TS.read()
  data=json.loads(response)
  newList = data['feeds']
  for x in newList:
    columns = ', '.join(x.keys())
    placeholders = '"'+'", "'.join(map(str, x.values()))+'"'
    print(x['entry_id'])
    if x['entry_id'] > ultimoID:
      query = 'INSERT INTO umidade (%s) VALUES (%s)' % (columns, placeholders)
      print(query)
      cursor.execute(query)
      conn.commit()   
      verificaNivel(alerta)    
  break
conn.close()
TS.close()

