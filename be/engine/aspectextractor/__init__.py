import spacy, time

from engine import utilities

class AspectExtractor:
  """An class that will generate aspect data from review data.
  """
  
  def generate_aspect_data(self, engine_db_conn, remake=False):
    """Generate aspect data at engine database from review data in the same database

    Args:
        engine_db_conn (Connection): sqlite3 connection to the engine database
        remake (bool): wheter to remake existing aspect data or not
    """

    print("Generating aspect data...")
    
    if utilities.table_exists(engine_db_conn, 'aspect'):
      if remake:
        engine_db_conn.execute("DROP TABLE aspect")
      else:
        print("  Found existing aspect data!")
        return

    cur = engine_db_conn.cursor()
    cur.execute("""
      CREATE TABLE aspect (
        review_id INTEGER,
        aspect TEXT,
        description TEXT,
        FOREIGN KEY (review_id) 
          REFERENCES review (rowid)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
      )
    """)
    
    print("  Reading review data...")
    reviews = []
    for i in cur.execute("SELECT review FROM review"):
      sent = i[0].replace("\\\'", "'")
      reviews.append(sent)

    print("  Extracting aspect data from reviews...")
    aspects = []
    nlp = spacy.load("en_core_web_sm")
    review_count = len(reviews)
    start_time = time.perf_counter()
    last_print = start_time - 10
    for i, sentence in enumerate(reviews):
      now = time.perf_counter()
      if (now - last_print > 1) or (i == review_count-1):
        spent_time = now - start_time
        print(f"\r    Progress: {i+1}/{review_count} ({spent_time:.2f}s, ETA: {(review_count-(i+1))*(spent_time/(i+1)):.2f}s)", end="")
        last_print = now
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
    print()

    print("  Inserting aspect data to aspect table...")
    for i in range(len(aspects)):
      a = aspects[i]['aspect'].replace("'","''")
      d = aspects[i]['description'].replace("'","''")
      cur.execute(f"INSERT INTO aspect VALUES ({i}, '{a}', '{d}')")

    engine_db_conn.commit()