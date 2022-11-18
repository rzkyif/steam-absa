import hug, json, argparse
from engine import Engine

SUPPORTED_COMMANDS = ['prepare', 'remake']

engine = Engine('../data/data.sqlite3')

@hug.get('/api/query')
def query(q: hug.types.cut_off(255), cors: hug.directives.cors = '*'):      
  result = engine.query(q)
  return json.dumps(result)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'command', metavar='command', 
    choices=SUPPORTED_COMMANDS, 
    help=f'What to do. Options: {", ".join(SUPPORTED_COMMANDS)}'
  )
  args = parser.parse_args()

  if args.command == 'prepare':
    engine.prepare_engine_db()
  elif args.command == 'remake':
    engine.prepare_engine_db(True)

