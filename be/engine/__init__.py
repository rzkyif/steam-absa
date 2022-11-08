from informationretriever import InformationRetriever
from aspectextractor import AspectExtractor
from sentimentanalyzer import SentimentAnalyzer

import sqlite3

DEFAULT_ENGINE_DB_PATH = './db.sqlite'

class Engine:
  """Main engine for all operations.
  """

  def initialize_engine_db(self, data_db_path):
    """Create engine database (containing relevant review data, aspect data, and sentiment data) by using aspect extractor and aspect based sentiment analyzer.

    Args:
        data_db_path (str): path to review data SQLite database
    """
    engine_db_conn = sqlite3.connect(self.engine_db_path)

    # copy relevant review data from review data SQLite database to engine database
    engine_db_conn.execute("""
      CREATE TABLE IF NOT EXISTS game (
        name TEXT
      )
    """)
    engine_db_conn.execute("""
      CREATE TABLE IF NOT EXISTS review (
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
    engine_db_conn.execute('ATTACH DATABASE ? AS data', data_db_path)
    engine_db_conn.execute('INSERT INTO review SELECT username, review, review_url FROM data.review')
    engine_db_conn.commit()

    # generate aspect data from relevant review data stored in engine database
    self.aspect_extractor.generate_aspect_data(engine_db_conn)

    # generate sentiment data from relevant review data and aspect data
    self.sentiment_analyzer.generate_sentiment_data(engine_db_conn)

    return engine_db_conn

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
