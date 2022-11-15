import hug
import json
from engine import Engine

engine = Engine('./data/data.sqlite3')

@hug.get('/api/query')
def query(q: hug.types.cut_off(255), cors: hug.directives.cors = '*'):      
  result = engine.query(q)
  return json.dumps(result)

@hug.post('/api/prepare')
def prepare(cors: hug.directives.cors = '*'):      
  try:
    engine.prepare_engine_db()
  except:
    return False
  return True