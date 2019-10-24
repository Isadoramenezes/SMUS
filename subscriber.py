import urllib.request
import json
import time
import sqlite3
from pprint import pprint


conn = sqlite3.connect('database.db')
cursor = conn.cursor()


while True:
  TS = urllib.request.urlopen("https://api.thingspeak.com/channels/879252/fields/1.json?results=5")

  response = TS.read()
  data=json.loads(response)
  #pprint(data)
  b = data['channel']['field1']
  #print (b)
  time.sleep(1) 

  newList = data['feeds']

  for x in newList:
    columns = ', '.join(x.keys())
    placeholders = '"'+'", "'.join(map(str, x.values()))+'"'
    query = 'INSERT INTO umidade (%s) VALUES (%s)' % (columns, placeholders)
    print(query)
    cursor.execute(query)
    conn.commit()
  break
conn.close()
TS.close()

