import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

from libs.DataImporter import DataImporter
from sklearn.decomposition import PCA
from entities.Storage import Storage
from libs.TFIDF import TFIDF
from mpl_toolkits.mplot3d import Axes3D
from libs.DataImporter import DataImporter
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold
from libs.Preprocessor import Preprocessor
import time


def map_bool(x):
	if x == 1:
		return True
	return False

def import_data(filename):
	print(f"Import {filename}")
	importer = DataImporter(filename)
	return importer.get_data()

def fold_data(data, k = 2):
	print(f"Fold data with k = {k}")
	kf = KFold(n_splits=k, shuffle=True, random_state=2)
	for train, test in kf.split(data):
		return train, test

def preprocess_data(data, selected_attr):
	print(f"Preprocess data...")
	preprocessor = Preprocessor()
	result = []
	for i, review in enumerate(data['Review']):
		result.append(" ".join(preprocessor.selected_preprocess(review, selected_attr)))
		print(f"Review {i + 1} preprocessed")
	return result

storage = Storage()

particle = storage.load('./pickle/pso-3.pckl')
data = storage.load('./pickle/default-1541653057.8427656.pckl')
train_idx, test_idx = fold_data(data)
pos = particle.position.astype(bool)
pos = [map_bool(x) for x in pos]
selected_tfidf = TFIDF(data.iloc[train_idx]['Review'])
features = np.array(list(selected_tfidf.termIndex.keys()))
features = features[pos]

data = import_data('../data/Avg_55,26.xlsx')
data['Review'] = preprocess_data(data, features)
storage.save(data, f"pickle/selected-3.pckl")
# data = storage.load('./pickle/selected-1542024722.200629.pckl')
for review, label in zip(data["Review"], data["Label"]):
	print(label, review)
tfidf = TFIDF(data["Review"])
english_labels = {
	"Berdampak positif": "Berdampak positif",
	"Berdampak negatif": "Berdampak negatif",
	"Netral": "Netral"	
}
groups = {
	"Berdampak positif": "green",
	"Berdampak negatif": "red",
	"Netral": "blue"	
}
translated_labels = [english_labels[label] for label in data["Label"]]
colors = np.array([groups[x] for x in translated_labels])

pca = PCA(n_components=2).fit(tfidf.weights)
data2D = pca.transform(tfidf.weights)
x_std = np.std(data2D[:, 0])
y_std = np.std(data2D[:, 1])

cleaned_data = storage.load("pickle/default-1541653057.8427656.pckl")
tfidf = TFIDF(cleaned_data["Review"])
pca = PCA(n_components=2).fit(tfidf.weights)
cleaned_data2D = pca.transform(tfidf.weights)
cleaned_x_std = np.std(cleaned_data2D[:, 0])
cleaned_y_std = np.std(cleaned_data2D[:, 1])

# plt.title("Distribusi Titik Data Ulasan Grafik Dirty vs Clean")

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(1, 2, sharey=True)
axarr[0].set_title("Before PSO")
axarr[0].set_xlabel("Komponen 1")
axarr[0].set_ylabel("Komponen 2")
# axarr[0].set_xlim(-0.6, 0.8)

axarr[1].set_title("After PSO")
axarr[1].set_xlabel("Komponen 1")
axarr[1].set_ylabel("Komponen 2")
axarr[1].set_xlim(-0.25, 0.75)

for label in set(data["Label"]):
	axarr[0].scatter(data2D[data[data["Label"] == label].index.values][:,0], data2D[data[data["Label"] == label].index.values][:,1], c=colors[data[data["Label"] == label].index.values], label=english_labels[label], edgecolors='black')

for label in set(cleaned_data['Label']):
	axarr[1].scatter(cleaned_data2D[cleaned_data[cleaned_data['Label'] == label].index.values][:,0] / 1000, cleaned_data2D[cleaned_data[cleaned_data['Label'] == label].index.values][:,1], c=colors[cleaned_data[cleaned_data['Label'] == label].index.values], label=english_labels[label], edgecolors='black')

axarr[0].legend(loc="upper right")
axarr[0].grid()

axarr[1].legend(loc="upper right")
axarr[1].grid()

plt.show()