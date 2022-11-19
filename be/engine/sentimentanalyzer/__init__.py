import spacy, time

from engine import utilities
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", top_k=None, model="cardiffnlp/twitter-roberta-base-sentiment-latest")

class SentimentAnalyzer:
  """An class that will generate sentiment data from review data and aspect data.
  """
  
  def generate_sentiment_data(self, engine_db_conn, remake=False):
    """Generate sentiment data at engine database from review data and aspect data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
        remake (bool): wheter to remake existing sentiment data or not
    """

    print("Generating sentiment data...")

    if utilities.table_exists(engine_db_conn, 'sentiment') and not remake:
      print("  Found existing sentiment data!")
      return

    engine_db_conn.execute("DROP TABLE IF EXISTS sentiment")
    engine_db_conn.execute("""
      CREATE TABLE sentiment (
        aspect_id INTEGER,
        sentiment TEXT,
        FOREIGN KEY (aspect_id) 
          REFERENCES aspect (rowid)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
      )
    """)

    print("    Turning aspect data to sentiment data...")
    nlp = spacy.load("en_core_web_sm")
    cur = engine_db_conn.cursor()
    cur2 = engine_db_conn.cursor()
    i = 0
    start_time = time.perf_counter()
    last_print = start_time - 10
    cur.execute("SELECT count(rowid) FROM aspect")
    review_count = cur.fetchone()[0]
    for aspect_data in cur.execute("SELECT rowid, description FROM aspect"):
      now = time.perf_counter()
      if (now - last_print > 1) or (i == review_count-1):
        spent_time = now - start_time
        print(f"\r      Progress: {i+1}/{review_count} ({spent_time:.2f}s, ETA: {(review_count-(i+1))*(spent_time/(i+1)):.2f}s)", end="")
        last_print = now

      aspect_id, description = aspect_data

      negative, neutral, positive = sentiment_pipeline(description)[0]
      if neutral['score'] < 0.3:
        if positive['score'] > negative['score']:
          cur2.execute("INSERT INTO sentiment VALUES (?, '+')", [aspect_id])
        else:
          cur2.execute("INSERT INTO sentiment VALUES (?, '-')", [aspect_id])

      i += 1
    engine_db_conn.commit()
    print()