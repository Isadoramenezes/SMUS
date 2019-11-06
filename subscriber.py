import urllib.request
import json
import sqlite3
import functools
import operator


alerta = 50

def buscaID():
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  select = cursor.execute("SELECT entry_id FROM umidade WHERE entry_id = (SELECT MAX(entry_id) FROM umidade)")
  idAtual = cursor.fetchall()
  conn.close()
  leituraAtual = idAtual[0]
  ultimoID = functools.reduce(operator.add, (leituraAtual))
  print("Ultimo ID")
  print(ultimoID)
  return ultimoID

def verificaNivel(alerta):
  status = False
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  cursor.execute("""
    SELECT field1 FROM umidade
    WHERE entry_id = (SELECT MAX(entry_id) FROM umidade)
  """)
  nivelAtual = cursor.fetchall()
  listaAtual = nivelAtual[0]
  nivelInteiro = functools.reduce(operator.add, (listaAtual))
  nivelInteiro = int(nivelInteiro)
  if nivelInteiro > alerta:
    status = True    
  conn.close()
  return status

def subscriber():
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  while True:
    TS = urllib.request.urlopen("https://api.thingspeak.com/channels/879252/fields/1.json?results=1")
    response = TS.read()
    data=json.loads(response)
    newList = data['feeds']
    for x in newList:
      columns = ', '.join(x.keys())
      placeholders = '"'+'", "'.join(map(str, x.values()))+'"'
      print("ID Atual")
      print(x['entry_id'])
      if x['entry_id'] > buscaID():
        query = 'INSERT INTO umidade (%s) VALUES (%s)' % (columns, placeholders)
        print(query)
        cursor.execute(query)
        conn.commit()   
        verificaNivel(alerta)    
    break
  conn.close()
  TS.close()
  print("###### VERIFICA ALERTA #####")
  print(verificaNivel(alerta))
  
  sinalAlerta = verificaNivel(alerta)
  print("Sinal Alerta")
  print(sinalAlerta)

  return sinalAlerta
  
sinalAlerta = subscriber()
subscriber()




