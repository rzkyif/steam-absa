import utilities
import sqlite3

from .informationretriever import InformationRetriever
from .aspectextractor import AspectExtractor
from .sentimentanalyzer import SentimentAnalyzer

DEFAULT_ENGINE_DB_PATH = './engine.sqlite3'

class Engine:
  """Main engine for all operations.
  """


  def initialize_engine_db(self, data_db_path):
    """Create basic engine database containing relevant review data.

    Args:
        data_db_path (str): path to review data SQLite database
    """
    print('Preparing engine database...')
    engine_db_conn = sqlite3.connect(self.engine_db_path)

    # copy relevant review data from review data SQLite database to engine database
    if not utilities.table_exists(engine_db_conn, 'review'):
      print(f"  Loading data from {data_db_path}...")
      engine_db_conn.execute("""
        CREATE TABLE game (
          name TEXT
        )
      """)
      engine_db_conn.execute("""
        CREATE TABLE review (
          game_id INTEGER,
          username TEXT,
          review TEXT,
          review_url TEXT,
          FOREIGN KEY (game_id) 
            REFERENCES game (rowid)
              ON DELETE CASCADE
              ON UPDATE NO ACTION
        )
      """)
      engine_db_conn.execute('ATTACH DATABASE ? AS data', [data_db_path])
      engine_db_conn.execute('INSERT INTO game(rowid, name) SELECT rowid, name FROM data.game')
      engine_db_conn.execute('INSERT INTO review(game_id, username, review, review_url) SELECT game_id, username, review, review_url FROM data.review')
      engine_db_conn.commit()
      print("    Done!")
    else:
      print("  Existing engine database found!")

    return engine_db_conn


  def prepare_engine_db(self, remake=False):
    """Generate aspect data and sentiment data using aspect extractor and aspect based sentiment analyzer
    """

    # generate aspect data
    self.aspect_extractor.generate_aspect_data(self.engine_db_conn, remake)

    # generate sentiment data
    self.sentiment_analyzer.generate_sentiment_data(self.engine_db_conn, remake)

    self.prepared = True


  def query(self, query, count=20, skip=0, game_filter=None):
    """Return Steam review data for reviews that match the query.

    Args:
        query (str): query string

    Returns:
        List[object]: list of review data
    """
    review_id_list = self.information_retriever.retrieve(self.engine_db_conn, query, count, skip, game_filter)
    cur = self.engine_db_conn.cursor()

    results = []
    for [review_id, _] in review_id_list:
      cur.execute("SELECT game_id, username, review, review_url FROM review WHERE rowid = ?", [review_id])
      [game_id, username, review, review_url] = cur.fetchone()
      sentiments = []
      cur.execute("SELECT aspect, sentiment FROM aspect, sentiment WHERE aspect.review_id = ? AND sentiment.aspect_id = aspect.rowid", [review_id])
      for [aspect, sentiment] in cur.fetchall():
        sentiments.append((aspect, sentiment))
      results.append({
        'game_id': game_id,
        'username': username,
        'review': review,
        'review_url': review_url,
        'sentiments': sentiments
      })

    return results


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
    self.engine_db_conn = self.initialize_engine_db(data_db_path)
    self.prepared = False
