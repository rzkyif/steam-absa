import hug, json, argparse
from engine import Engine

SUPPORTED_COMMANDS = ['prepare', 'remake']

engine = Engine('../data/data.sqlite3')

@hug.get('/api/query')
def query(q: hug.types.cut_off(255), count: hug.types.number=20, skip: hug.types.number=0, game_filter: hug.types.comma_separated_list=None, cors: hug.directives.cors = '*'):      
  result = engine.query(q, count, skip, list(map(lambda x: int(x), game_filter)))
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

