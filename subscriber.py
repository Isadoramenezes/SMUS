import urllib.request
import json
import sqlite3
import functools
import operator

def consultaAlerta():
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  cursor.execute("SELECT nivel_alerta FROM controle_de_nivel WHERE id = (SELECT MAX(id) FROM controle_de_nivel)")
  alertaBanco = cursor.fetchall()
  conn.close()
  alertaBancoAtual = alertaBanco[0]
  ultimoAlerta = functools.reduce(operator.add, (alertaBancoAtual))
  ultimoAlerta = int(ultimoAlerta)
  return ultimoAlerta

def buscaID():
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  cursor.execute("SELECT entry_id FROM umidade WHERE entry_id = (SELECT MAX(entry_id) FROM umidade)")
  idAtual = cursor.fetchall()
  conn.close()
  leituraAtual = idAtual[0]
  ultimoID = functools.reduce(operator.add, (leituraAtual))
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
    alertaAtual = consultaAlerta()

    for x in newList:
      columns = ', '.join(x.keys())
      placeholders = '"'+'", "'.join(map(str, x.values()))+'"'
      if x['entry_id'] > buscaID():
        query = 'INSERT INTO umidade (%s) VALUES (%s)' % (columns, placeholders)
        cursor.execute(query)
        conn.commit() 
        verificaNivel(alertaAtual)    
    break
  conn.close()
  TS.close()
  sinalAlerta = verificaNivel(alertaAtual)
  return sinalAlerta
subscriber()




