class AspectExtractor:
  """An class that will generate aspect data from review data.
  """
  
  def generate_aspect_data(self, engine_db_conn):
    """Generate aspect data at engine database from review data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
    """

    engine_db_conn.execute("""
      CREATE TABLE aspect (
        review_id INTEGER,
        aspect TEXT,
        FOREIGN KEY (review_id) 
          REFERENCES review (rowid)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
      )
    """)

    # TODO: read 'review' table, insert aspect data into 'aspect' table

    engine_db_conn.commit()
    pass