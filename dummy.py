# from sklearn.decomposition import PCA
# from entities.Storage import Storage
# from libs.TFIDF import TFIDF
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np

# s = Storage()
# data = s.load("data/preprocessed/preprocessed.pckl")
# tfidf = TFIDF(data["Review"])
# groups = {
# 	"Berdampak positif": "green",
# 	"Berdampak negatif": "red",
# 	"Netral": "blue"
# }
# colors = np.array([groups[x] for x in data["Label"]])

# pca = PCA(n_components=2).fit(tfidf.weights)
# data2D = pca.transform(tfidf.weights)

# plt.xlabel("Komponen 1")
# plt.ylabel("Komponen 2")
# plt.title("Sebaran Data Setelah Dipraproses")

# for label in set(data["Label"]):
# 	plt.scatter(data2D[data[data["Label"] == label].index.values][:,0], data2D[data[data["Label"] == label].index.values][:,1], c=colors[data[data["Label"] == label].index.values], label=label, edgecolors='black')
# plt.legend()
# plt.grid()
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")
# pca = PCA(n_components=3).fit(tfidf.weights)
# data3D = pca.transform(tfidf.weights)
# for label in set(data["Label"]):
# 	ax.scatter(data3D[data[data["Label"] == label].index.values][:,0], data3D[data[data["Label"] == label].index.values][:,1], c=colors[data[data["Label"] == label].index.values], label=label, edgecolors='black')
# ax.legend()
# ax.grid()
# ax.set_xlabel('Komponen 1')
# ax.set_ylabel('Komponen 2')
# ax.set_zlabel('Komponen 3')

# plt.show()

# import numpy as np, matplotlib.pyplot as plt

# c45_scores = np.array([47.92, 54.17, 52.63, 42.11, 42.11, 47.37, 44.21, 43.16, 47.37, 47.37])
# pso_c45_scores_1 = np.array([51.04, 55.21, 53.68, 47.37, 45.26, 51.58, 47.37, 43.16, 50.53, 48.42])
# pso_c45_scores_2 = np.array([50.00, 55.21, 53.68, 44.21, 45.26, 49.47, 47.37, 43.16, 52.63, 46.32])
# pso_c45_scores_3 = np.array([50.00, 56.25, 54.74, 46.32, 45.26, 49.47, 47.37, 44.21, 52.63, 47.37])
# print(np.mean(c45_scores))
# print(pso_c45_scores_1 - c45_scores, np.mean(pso_c45_scores_1))
# print(pso_c45_scores_2 - c45_scores, np.mean(pso_c45_scores_2))
# print(pso_c45_scores_3 - c45_scores, np.mean(pso_c45_scores_3))
# result_mean_1 = np.mean(pso_c45_scores_1 - c45_scores)
# result_mean_2 = np.mean(pso_c45_scores_2 - c45_scores)
# result_mean_3 = np.mean(pso_c45_scores_3 - c45_scores)
# x_axis = np.linspace(0, 10, 10)
# y_axis = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# plt.plot(x_axis, c45_scores, label="Akurasi C4.5")
# plt.scatter(x_axis, c45_scores)
# # plt.plot(x_axis, pso_c45_scores_1, label="Akurasi PSO - C4.5 Konfigurasi 1")
# # plt.scatter(x_axis, pso_c45_scores_1)
# plt.plot(x_axis, pso_c45_scores_2, label="Akurasi PSO - C4.5 Konfigurasi 2")
# plt.scatter(x_axis, pso_c45_scores_2)
# # plt.plot(x_axis, pso_c45_scores_3, label="Akurasi PSO - C4.5 Konfigurasi 3")
# # plt.scatter(x_axis, pso_c45_scores_3)
# plt.grid()
# plt.legend()
# plt.xlabel("k")
# plt.ylabel("Akurasi")
# plt.yticks(y_axis)
# plt.title(f"Hasil Perbandingan Akurasi C4.5 dan PSO - C4.5 Konfigurasi 2 (+{round(result_mean_2, 2)}%)")
# plt.show()


from entities.Storage import Storage

s = Storage()
for i in range(10):
	clf = s.load(f"data/models/tree{i + 1}.pckl")
	print(round(clf.scores * 100, 2))