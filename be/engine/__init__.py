from .informationretriever import InformationRetriever
from .aspectextractor import AspectExtractor
from .sentimentanalyzer import SentimentAnalyzer

import utilities
import sqlite3

DEFAULT_ENGINE_DB_PATH = './engine.sqlite3'

class Engine:
  """Main engine for all operations.
  """


  def initialize_engine_db(self, data_db_path):
    """Create basic engine database containing relevant review data.

    Args:
        data_db_path (str): path to review data SQLite database
    """
    engine_db_conn = sqlite3.connect(self.engine_db_path)

    # copy relevant review data from review data SQLite database to engine database
    if not utilities.table_exists(engine_db_conn, 'review'):
      engine_db_conn.execute("""
        CREATE TABLE game (
          name TEXT
        )
      """)
      engine_db_conn.execute("""
        CREATE TABLE review (
          game_id INTEGER,
          username TEXT,
          review_url TEXT,
          review TEXT,
          FOREIGN KEY (game_id) 
            REFERENCES game (rowid)
              ON DELETE CASCADE
              ON UPDATE NO ACTION
        )
      """)
      engine_db_conn.execute('ATTACH DATABASE ? AS data', [data_db_path])
      engine_db_conn.execute('INSERT INTO game SELECT rowid, name FROM data.game')
      engine_db_conn.execute('INSERT INTO review SELECT game_id, username, review, review_url FROM data.review')
      engine_db_conn.commit()

    return engine_db_conn


  def prepare_engine_db(self):
    """Generate aspect data and sentiment data using aspect extractor and aspect based sentiment analyzer
    """

    # generate aspect data
    self.aspect_extractor.generate_aspect_data()

    # generate sentiment data
    self.sentiment_analyzer.generate_sentiment_data()

    self.prepared = True


  def query(self, query):
    """Return Steam review data for reviews that match the query.

    Args:
        query (str): query string

    Returns:
        List[object]: list of review data
    """
    return self.information_retriever.retrieve(self.engine_db, query)

  def __init__(self, data_db_path, engine_db_path=DEFAULT_ENGINE_DB_PATH):
    """Start up a new engine.

    Args:
        engine_db_path (str, optional): path to aspect data SQLite database. Defaults to 'db.sqlite'.
        data_db_path (str, optional): path to review data SQLite database. Defaults to 'data/data.sqlite'.
    """

    # load engine components
    self.information_retriever = InformationRetriever()
    self.aspect_extractor = AspectExtractor()
    self.sentiment_analyzer = SentimentAnalyzer()

    # variables
    self.engine_db_path = engine_db_path
    self.engine_db = self.initialize_engine_db(data_db_path)
    self.prepared = False
