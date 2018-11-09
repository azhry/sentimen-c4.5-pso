import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

from libs.DataImporter import DataImporter
from sklearn.decomposition import PCA
from entities.Storage import Storage
from libs.TFIDF import TFIDF
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

s = Storage()
data = s.load("pickle/default-1541653057.8427656.pckl")
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

# importer = DataImporter('./outlier_distance.xlsx')
# outlier_data = importer.get_data()
# outlier_data['label'] = data['Label']
# cleaned_data = outlier_data.loc[outlier_data['outlier'] == False]
# s.save(cleaned_data, './pickle/cleaned_data.pckl')
# cleaned_data = outlier_data.loc[outlier_data['outlier'] == False].as_matrix(columns=outlier_data.columns[:1982])
# s.save(cleaned_data, './pickle/cleaned_data.pckl')
cleaned_data = s.load('./pickle/cleaned_data.pckl')
cleaned_data = cleaned_data.reset_index()
cleaned_matrix = cleaned_data.as_matrix(columns=cleaned_data.columns[:1982])

pca = PCA(n_components=2).fit(cleaned_matrix)
cleaned_data2D = pca.transform(cleaned_matrix)
cleaned_x_std = np.std(cleaned_data2D[:, 0])
cleaned_y_std = np.std(cleaned_data2D[:, 1])

# plt.title("Distribusi Titik Data Ulasan Grafik Dirty vs Clean")

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(1, 2, sharey=True)
axarr[0].set_title("Before removing outlier")
axarr[0].set_xlabel("Komponen 1")
axarr[0].set_ylabel("Komponen 2")

axarr[1].set_title("After removing outlier")
axarr[1].set_xlabel("Komponen 1")
axarr[1].set_ylabel("Komponen 2")

for label in set(data["Label"]):
	axarr[0].scatter(data2D[data[data["Label"] == label].index.values][:,0], data2D[data[data["Label"] == label].index.values][:,1], c=colors[data[data["Label"] == label].index.values], label=english_labels[label], edgecolors='black')

for label in set(cleaned_data['label']):
	axarr[1].scatter(cleaned_data2D[cleaned_data[cleaned_data['label'] == label].index.values][:,0] / 1000, cleaned_data2D[cleaned_data[cleaned_data['label'] == label].index.values][:,1], c=colors[cleaned_data[cleaned_data['label'] == label].index.values], label=english_labels[label], edgecolors='black')

axarr[0].legend(loc="upper right")
axarr[0].grid()

axarr[1].legend(loc="upper right")
axarr[1].grid()

plt.show()