class InformationRetriever:
  """A class that will retrieve review data that corresponds to queries
  """

  def retrieve(self, engine_db_conn, query):
    """Retrieve review data in engine database that corresponds to the query

    Args:
        engine_db_conn (Connection): sqlite3 connection to engine database
        query (str): query string

    Returns:
        List[object]: list of review data that corresponds to query
    """    
    
    # TODO: use engine database connection and information retrieval to get reviews that corresponds to query

    return []