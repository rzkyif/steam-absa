import sqlite3
import json
import os
import sys

# configure which columns to take from json files
DB_PATH = 'data/data.sqlite3'
COLUMNS = ['username', 'review_url', 'review']

# create sqlite database
if os.path.exists(DB_PATH): 
    check = input("Database already exists, remake? (y/N) ")
    if check.lower() == 'y':
        os.remove(DB_PATH)
    else:
        sys.exit('Database already exists.')
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute(f"CREATE TABLE reviews(game_id, {', '.join(COLUMNS)})")
cur.execute(f"CREATE TABLE game(name)")

# open all review data, load into sqlite3 database
games = ["Arma_3", "Counter_Strike_Global_Offensive", "Counter_Strike", "Dota_2", "Football_Manager_2015", "Garrys_Mod", "Grand_Theft_Auto_V", "Sid_Meiers_Civilization_5", "Team_Fortress_2", "The_Elder_Scrolls_V", "Warframe"]
allreview = []
print("Loading .jsonlines files...")
for id, game in enumerate(games):
    with open("data/raw/"+game+".jsonlines", 'r') as f:
        print(f"  Processing {game} data...")
        cur.execute(f"INSERT INTO game(rowid, name) VALUES (?, ?)", [id, game.replace('_', ' ')])
        for line in f:
            object = json.loads(line)
            cur.execute(f"INSERT INTO reviews VALUES (?, ?, ?, ?)", [id] + [object[x] for x in COLUMNS])
con.commit()
print(f"Completed!")