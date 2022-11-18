import spacy, time

from engine import utilities

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

    engine_db_conn.execute("DROP TABLE sentiment")
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
    if utilities.table_exists(engine_db_conn, 'sentiment_amod') and not remake:
      print("    Found existing amod data!")
    else:
      print("    Building new amod data...")
      engine_db_conn.execute("DROP TABLE sentiment_amod")
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
      i = 0
      start_time = time.perf_counter()
      last_print = start_time - 10
      cur.execute("SELECT count(rowid) FROM review")
      review_count = cur.fetchone()[0]
      for review_data in cur.execute("SELECT rowid, review FROM review"):
        now = time.perf_counter()
        if (now - last_print > 1) or (i == review_count-1):
          spent_time = now - start_time
          print(f"\r      Progress: {i+1}/{review_count} ({spent_time:.2f}s, ETA: {(review_count-(i+1))*(spent_time/(i+1)):.2f}s)", end="")
          last_print = now
        [rowid, review] = review_data
        doc = nlp(review)
        for token in doc:
          if token.dep_ != 'amod': continue
          print(f"      Found amod: {rowid} {token.text} {token.head.text}")
          cur2.execute("INSERT INTO sentiment_amod VALUES (?, ?, ?)", [rowid, token.text, token.head.text])
        i += 1
      engine_db_conn.commit()
      print()
  
    # TODO: read 'review' table and 'aspect' table, populate 'sentiment' table with sentiment data

    engine_db_conn.commit()