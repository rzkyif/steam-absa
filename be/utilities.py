def table_exists(conn, table_name):
  cur = conn.cursor()
  cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='?'", [table_name])
  return cur.fetchone()[0] == 1