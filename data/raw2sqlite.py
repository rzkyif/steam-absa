# TODO: make code to convert all .jsonlines file to one .sqlite file
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer 
import stanfordnlp
import sqlite3

def fun(x):
    return x.replace("'","''")

# open all json
names = ["Arma_3", "Counter_Strike_Global_Offensive", "Counter_Strike", "Dota_2", "Football_Manager_2015", "Garrys_Mod", "Grand_Theft_Auto_V", "Sid_Meiers_Civilization_5", "Team_Fortress_2", "The_Elder_Scrolls_V", "Warframe"]
allreview = []
for i in names:
    name = "data/raw/"+i+".jsonlines"
    df = pd.read_json(name, lines=True)
    reviews = df['review'].tolist()
    allreview += reviews
# print(allreview)
# print(allreview)
allreview = list(map(fun, allreview))
# print(c)
# all = ",".join(c)
# print(all)
con = sqlite3.connect("data/reviews.db")
cur = con.cursor()

cur.execute("CREATE TABLE reviews(review)")

params = {'allreview':allreview}
for i in allreview:
    print(f"INSERT INTO reviews VALUES ('{i}')")
    cur.execute(f"INSERT INTO reviews VALUES ('{i}')")
# cur.executemany("INSERT INTO reviews VALUES(?)", allreview)
con.commit()
