import hug
import json
from engine import Engine

engine = Engine('./db.sqlite')

@hug.get('/api/query')
def query(q: hug.types.cut_off(255), response = None):
  if not engine.started: return json.dumps({
    'error': 'Engine not started! Send POST request to /api/start first!'
  })
      
  result = engine.query(q)
  return json.dumps(result)

@hug.post('/api/start')
def query():
  engine.start()