import sqlite3, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy.linalg import norm

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
    
    datas = []
    comments = []
    cur = engine_db_conn.cursor()
    for row in cur.execute("SELECT * from review"):
      comment = row[3].replace("\\\'", "'")
      data = (row[0], row[1], row[2], comment)
      datas.append(data)
      comments.append(comment)

    vec = TfidfVectorizer()
    document_vec = vec.fit_transform(comments)
    query_vec = vec.transform([query])
    query_array = np.array(query_vec.toarray()[0])

    sims = []
    for dv in document_vec:
      document_array = np.array(dv.toarray())
      sim = np.dot(document_array, query_array) / (norm(document_array) * norm(query_array)) if (norm(document_array) * norm(query_array)) != 0 else 0.0
      sims.append(float(sim))
    
    # Tuple reviews: (game_id, username, review_url, review, cosine_similarity)
    reviews = []
    for i in range(len(datas)):
      reviews.append((datas[i][0], datas[i][1], datas[i][2], datas[i][3], sims[i]))

    reviews.sort(key=lambda tup: tup[4], reverse=True)
    
    for i in range(5):
      print(reviews[i])

    return reviews

if __name__=='__main__':
  ir = InformationRetriever()
  con = sqlite3.connect('../../../data/data.sqlite3')
  ir.retrieve(con, "gta")