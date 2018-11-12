import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

import numpy as np, random, math, pandas as pd, time
from libs.TFIDF import TFIDF
from libs.C45 import C45
from entities.Storage import Storage
from sklearn.model_selection import KFold
from libs.Preprocessor import Preprocessor
from libs.DataImporter import DataImporter

def preprocess_data(data, selected_words):
	print(f"Preprocess data...")
	preprocessor = Preprocessor()
	result = []
	for i, review in enumerate(data['Review']):
		result.append(" ".join(preprocessor.preprocess(review)))
		print(f"Review {i + 1} preprocessed")
	return result

def map_bool(x):
	if x == 1:
		return True
	return False

def fold_data(data, k = 2):
	kf = KFold(n_splits=k, shuffle=True, random_state=2)
	for train, test in kf.split(data):
		return train, test

def import_data(filename):
	print(f"Import {filename}")
	importer = DataImporter(filename)
	return importer.get_data()

storage = Storage()
particle = storage.load('./pickle/pso-1.pckl')
pos = particle.position.astype(bool)
pos = [map_bool(x) for x in pos]
data = storage.load('./pickle/default-1541653057.8427656.pckl')
train_idx, test_idx = fold_data(data)
selected_tfidf = TFIDF(data.iloc[train_idx]['Review'])
features = np.array(list(selected_tfidf.termIndex.keys()))
features = features[pos]

new_data = import_data('../data/Avg_55,26.xlsx')
new_data['Review'] = preprocess_data(new_data, features)

storage.save(new_data, f"pickle/preprocessed-{time.time()}.pckl")

# kf = KFold(n_splits=10, shuffle=True, random_state=2)
# for i, (train, test) in enumerate(kf.split(data)):
# 	print("Train optimized")
# 	tfidf = TFIDF(data.iloc[train]["Review"])
# 	tfidf.weights = tfidf.remove_zero_tfidf(tfidf.weights, 0.5)
# 	tfidf.termIndex = {key:val for i, (key, val) in enumerate(tfidf.termIndex.items()) if key in features}
# 	clf = C45(tfidf, data.iloc[train])
# 	clf.train()
# 	result = clf.score(tfidf, data.iloc[test])

# 	print("Train unoptimized")
# 	tfidf = TFIDF(data.iloc[train]["Review"])
# 	tfidf.weights = tfidf.remove_zero_tfidf(tfidf.weights, 0.5)
# 	clf_unoptimized = C45(tfidf, data.iloc[train])
# 	clf_unoptimized.train()
# 	result_unoptimized = clf_unoptimized.score(tfidf, data.iloc[test])
# 	print(result_unoptimized, result)