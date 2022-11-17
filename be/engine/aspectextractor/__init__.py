import sqlite3, nltk, spacy


class AspectExtractor:
  """An class that will generate aspect data from review data.
  """
  
  def generate_aspect_data(self, engine_db_conn):
    """Generate aspect data at engine database from review data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
    """

    cur = engine_db_conn.cursor()
    # cur.execute("""
    #   CREATE TABLE aspect (
    #     review_id INTEGER,
    #     aspect TEXT,
    #     description TEXT,
    #     FOREIGN KEY (review_id) 
    #       REFERENCES review (rowid)
    #         ON DELETE CASCADE
    #         ON UPDATE NO ACTION
    #   )
    # """)
    
    reviews = []
    for i in cur.execute("SELECT * FROM reviews"):
      sent = i[0].replace("\\\'", "'")
      # print(sent)
      # break
      reviews.append(sent)

    aspects = []
    nlp = spacy.load("en_core_web_sm")
    for sentence in reviews:
      doc = nlp(sentence)
      descriptive_term = ''
      target = ''
      for token in doc:
        if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
          target = token.text
        if token.pos_ == 'ADJ':
          prepend = ''
          for child in token.children:
            if child.pos_ != 'ADV':
              continue
            prepend += child.text + ' '
          descriptive_term = prepend + token.text
      aspects.append({'aspect': target,
        'description': descriptive_term})

    print(aspects[5482:])
    for i in range(len(aspects)):
      a = aspects[i]['aspect'].replace("'","''")
      d = aspects[i]['description'].replace("'","''")
      cur.execute(f"INSERT INTO aspect VALUES ({i}, '{a}', '{d}')")

    engine_db_conn.commit()

if __name__ == "__main__":
  ass = AspectExtractor()
  con = sqlite3.connect("data/reviews.db")
  cur = con.cursor()
  ass.generate_aspect_data(con)