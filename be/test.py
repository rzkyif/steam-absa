import argparse, shutil, os, sqlite3

from engine import Engine

SUPPORTED_COMPONENTS = ['sentimentanalyzer', 'aspectextractor', 'informationretriever']


def test_sentiment_analyzer(engine):
  """TEST CODE FOR SENTIMENT ANALYZER COMPONENT

  Args:
      engine (Engine): the test engine
  """
  # engine.aspect_extractor.generate_aspect_data(engine.engine_db_conn)
  engine.sentiment_analyzer.generate_sentiment_data(engine.engine_db_conn)


def test_aspect_extractor(engine):
  """TEST CODE FOR ASPECT EXTRACTOR COMPONENT

  Args:
      engine (Engine): the test engine
  """
  engine.aspect_extractor.generate_aspect_data(engine.engine_db_conn)


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
  args = parser.parse_args()

  engine = Engine('../data/data.sqlite3', engine_db_path='./engine_test.sqlite3')

  if args.component == 'sentimentanalyzer':
    test_sentiment_analyzer(engine)
  elif args.component == 'aspectextractor':
    test_aspect_extractor(engine)
  elif args.component == 'informationretriever':
    test_information_retriever(engine)