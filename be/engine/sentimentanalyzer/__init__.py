class SentimentAnalyzer:
  """An class that will generate sentiment data from review data and aspect data.
  """
  
  def generate_sentiment_data(self, engine_db_conn):
    """Generate sentiment data at engine database from review data and aspect data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
    """

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

    # TODO: read 'review' table and 'aspect' table, populate 'sentiment' table with sentiment data

    engine_db_conn.commit()
    