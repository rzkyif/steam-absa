import hug
import json
from engine import Engine

engine = Engine('./db.sqlite')

@hug.get('/api/query')
def query(q: hug.types.cut_off(255), cors: hug.directives.cors = '*'):      
  result = engine.query(q)
  return json.dumps(result)