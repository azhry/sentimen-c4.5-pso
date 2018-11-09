import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

from libs.DataImporter import DataImporter
from libs.Preprocessor import Preprocessor
from libs.TFIDF import TFIDF
from libs.C45 import C45
from libs.PSO import PSO
from entities.Storage import Storage
from sklearn.model_selection import KFold
import time

def import_data(filename):
	print(f"Import {filename}")
	importer = DataImporter(filename)
	return importer.get_data()

def fold_data(data, k = 2):
	print(f"Fold data with k = {k}")
	kf = KFold(n_splits=k, shuffle=True, random_state=2)
	for train, test in kf.split(data):
		return train, test

def preprocess_data(data):
	print(f"Preprocess data...")
	preprocessor = Preprocessor()
	result = []
	for i, review in enumerate(data['Review']):
		result.append(" ".join(preprocessor.preprocess(review)))
		print(f"Review {i + 1} preprocessed")
	return result

# data = import_data('../data/Avg_55,26.xlsx')
# data['Review'] = preprocess_data(data)
storage = Storage()
# storage.save(data, f"pickle/default-{time.time()}.pckl")
data = storage.load("pickle/default-1541653057.8427656.pckl")
train, test = fold_data(data)
train_data = data.iloc[train]
test_data = data.iloc[test]

tfidf = TFIDF(train_data['Review'])
num_attrs = len(tfidf.termIndex)
# clf = C45(tfidf, data)
# clf.train()

# score = clf.score(tfidf, test_data)
# print(score) # 0.3630573248407643

pso = PSO(num_attrs, 20, 20, 0.7, 0.5, 0.99)
result = pso.exec(train_data, test_data)
storage.save(result, f"pickle/pso-1.pckl")