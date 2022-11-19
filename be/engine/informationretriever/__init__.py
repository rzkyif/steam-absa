import numpy as np, time
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy.linalg import norm

class InformationRetriever:
  """A class that will retrieve review data that corresponds to queries
  """

  def retrieve(self, engine_db_conn, query, count=20, skip=0, game_filter=None):
    """Retrieve review data in engine database that corresponds to the query

    Args:
        engine_db_conn (Connection): sqlite3 connection to engine database
        query (str): query string

    Returns:
        List[object]: list of review data that corresponds to query
    """    

    print(f"Processing query '{query}' ({count}, {skip}, {game_filter})...")
    cur = engine_db_conn.cursor()
    row_ids = []
    review_texts = []
    for row in cur.execute("SELECT game_id, review.rowid, review FROM sentiment LEFT JOIN aspect LEFT JOIN review WHERE sentiment.aspect_id = aspect.rowid AND aspect.review_id = review.rowid"):
      if game_filter is not None and row[0] not in game_filter: continue
      row_ids.append(row[1])
      review_texts.append(row[2].replace("\\\'", "'"))

    print("  Making document and query vectors...")
    vec = TfidfVectorizer()
    document_vec = vec.fit_transform(review_texts)
    query_vec = vec.transform([query])
    print("    Done!")

    print("  Calculating cosine similarities...")
    cosine_sims = []
    y = np.array([query_vec.toarray()[0]])

    document_count = len(row_ids)
    start_time = time.perf_counter()
    last_print = start_time - 10
    for i, dv in enumerate(document_vec):
      now = time.perf_counter()
      if (now - last_print > 1) or (i == document_count-1):
        spent_time = now - start_time
        print(f"\r    Progress: {i+1}/{document_count} ({spent_time:.2f}s, ETA: {(document_count-(i+1))*(spent_time/(i+1)):.2f}s)", end="    ")
        last_print = now

      x = np.array(dv.toarray())

      norms_X = np.sqrt((x * x).sum(axis=1))
      x /= norms_X[:, np.newaxis]
      norms_Y = np.sqrt((y * y).sum(axis=1))
      y /= norms_Y[:, np.newaxis]
      cosine_sim = np.dot(x, y.T)

      cosine_sims.append(float(cosine_sim))
    print()
    
    print("  Calculating result row ids...")
    reviews = [(row_ids[i], cosine_sims[i]) for i in range(len(row_ids))]
    reviews.sort(key=lambda review: review[1], reverse=True)
    print("    Done!")

    return reviews[skip:skip+count]