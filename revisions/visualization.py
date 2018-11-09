import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

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

plt.xlabel("Komponen 1")
plt.ylabel("Komponen 2")
plt.title("Distribusi Titik Data Ulasan Grafik 2D")

for label in set(data["Label"]):
	plt.scatter(data2D[data[data["Label"] == label].index.values][:,0], data2D[data[data["Label"] == label].index.values][:,1], c=colors[data[data["Label"] == label].index.values], label=english_labels[label], edgecolors='black')
plt.legend(loc="lower right")
plt.grid()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
pca = PCA(n_components=3).fit(tfidf.weights)
data3D = pca.transform(tfidf.weights)
for label in set(data["Label"]):
	ax.scatter(data3D[data[data["Label"] == label].index.values][:,0], data3D[data[data["Label"] == label].index.values][:,1], c=colors[data[data["Label"] == label].index.values], label=english_labels[label], edgecolors='black')
ax.legend(loc="lower left")
ax.grid()
ax.set_xlabel('Komponen 1')
ax.set_ylabel('Komponen 2')
ax.set_zlabel('Komponen 3')
plt.title("Distribusi Titik Data Ulasan Grafik 3D")

plt.show()