import spacy

from engine import utilities

class SentimentAnalyzer:
  """An class that will generate sentiment data from review data and aspect data.
  """
  
  def generate_sentiment_data(self, engine_db_conn):
    """Generate sentiment data at engine database from review data and aspect data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
    """

    print("Generating sentiment data...")
    engine_db_conn.execute("DROP TABLE IF EXISTS sentiment")
    engine_db_conn.execute("""
      CREATE TABLE sentiment (
        review_id INTEGER,
        aspect_id INTEGER
        sentiment TEXT,
        FOREIGN KEY (review_id) 
          REFERENCES review (rowid) 
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
        FOREIGN KEY (aspect_id) 
          REFERENCES aspect (rowid)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
      )
    """)

    print("  Checking amod data...")
    if utilities.table_exists(engine_db_conn, 'sentiment_amod'):
      print("    Found existing amod data!")
    else:
      print("    Building new amod data...")
      engine_db_conn.execute("""
        CREATE TABLE sentiment_amod (
          review_id INTEGER,
          adjective TEXT
          object TEXT,
          FOREIGN KEY (review_id) 
            REFERENCES review (rowid) 
              ON DELETE CASCADE
              ON UPDATE NO ACTION
        )
      """)
      engine_db_conn.commit()
      nlp = spacy.load("en_core_web_sm")
      cur = engine_db_conn.cursor()
      cur2 = engine_db_conn.cursor()
      for review_data in cur.execute("SELECT rowid, review FROM review"):
        [rowid, review] = review_data
        doc = nlp(review)
        for token in doc:
          if token.dep_ != 'amod': continue
          cur2.execute("INSERT INTO sentiment_amod VALUES (?, ?, ?)", [rowid, token.text, token.head.text])
      engine_db_conn.commit()
  
    # TODO: read 'review' table and 'aspect' table, populate 'sentiment' table with sentiment data

    engine_db_conn.commit()