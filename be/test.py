import argparse, os

from engine import Engine

SUPPORTED_COMPONENTS = ['sentimentanalyzer', 'aspectextractor', 'informationretriever']


def test_sentiment_analyzer(engine):
  """TEST CODE FOR SENTIMENT ANALYZER COMPONENT

  Args:
      engine (Engine): the test engine
  """
  engine.aspect_extractor.generate_aspect_data(engine.engine_db_conn)
  engine.sentiment_analyzer.generate_sentiment_data(engine.engine_db_conn, True)


def test_aspect_extractor(engine):
  """TEST CODE FOR ASPECT EXTRACTOR COMPONENT

  Args:
      engine (Engine): the test engine
  """
  engine.aspect_extractor.generate_aspect_data(engine.engine_db_conn, True)


def test_information_retriever(engine):
  """TEST CODE FOR INFORMATION RETRIEVER COMPONENT

  Args:
      engine (Engine): the test engine
  """
  engine.prepare_engine_db()
  engine.query('graphics')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'component', metavar='component', 
    choices=SUPPORTED_COMPONENTS, 
    help=f'Which component to test. Options: {", ".join(SUPPORTED_COMPONENTS)}'
  )
  parser.add_argument(
    '-c', '--clean', metavar='clean', 
    const=True, default=False, action='store_const', 
    help=f'Start with a clean database.'
  )
  args = parser.parse_args()

  if args.clean and os.path.exists("./engine_test.sqlite3"):
    os.remove('./engine_test.sqlite3')
  engine = Engine('../data/data.sqlite3', engine_db_path='./engine_test.sqlite3')

  if args.component == 'sentimentanalyzer':
    test_sentiment_analyzer(engine)
  elif args.component == 'aspectextractor':
    test_aspect_extractor(engine)
  elif args.component == 'informationretriever':
    test_information_retriever(engine)