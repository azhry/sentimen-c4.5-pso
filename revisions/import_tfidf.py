import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

import numpy as np, random, math, pandas as pd
from libs.TFIDF import TFIDF
from entities.Storage import Storage

storage = Storage()
data = storage.load('./pickle/default-1541653057.8427656.pckl')
tfidf = TFIDF(data['Review'])
print(len(tfidf.weights[0]))

df = pd.DataFrame(tfidf.weights)
df.to_excel('tfidf.xlsx')