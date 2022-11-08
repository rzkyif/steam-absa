class SentimentAnalyzer:
  """An class that will generate sentiment data from review data and aspect data.
  """
  def generate_sentiment_data(self, engine_db_conn):
    """Generate sentiment data at engine database from review data and aspect data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
    """
    # TODO: read 'review' table and 'aspect' table, create 'sentiment' table with sentiment data
    # 
    #       structure (maybe?) :
    # 
    #         CREATE TABLE sentiment (
    #           review_id INTEGER,
    #           aspect_id INTEGER
    #           sentiment TEXT,
    #           FOREIGN KEY (review_id) 
    #             REFERENCES review (rowid)
    #               ON DELETE CASCADE
    #               ON UPDATE NO ACTION,
    #           FOREIGN KEY (aspect_id) 
    #             REFERENCES aspect (rowid)
    #               ON DELETE CASCADE
    #               ON UPDATE NO ACTION
    #         )
    #       
    pass
    