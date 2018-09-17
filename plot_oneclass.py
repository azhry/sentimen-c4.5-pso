# from entities.Storage import Storage
# from libs.TFIDF import TFIDF
# from libs.C45 import C45
# from sklearn.metrics import classification_report
# import time
# from libs.PSO import PSO

# s = Storage()

# for i in range(10):
# 	train, test = s.load(f"data/folds/train{i + 1}.pckl"), s.load(f"data/folds/test{i + 1}.pckl")
# 	clf = s.load(f"data/models/tree{i + 1}.pckl")
# 	tfidf = TFIDF(train["Review"])
# 	tfidf.weights = tfidf.remove_zero_tfidf(tfidf.weights, 0.5)
# 	print(classification_report(test["Label"], clf.predict(tfidf, test["Review"])))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

precisions = np.array([83, 45, 17, 79, 48, 33, 75, 48, 71, 62, 48, 17, 72, 51, 50, 79, 53, 43, 90, 46, 50, 75, 40, 70, 75, 48, 33, 67, 57, 75])
recalls = np.array([62, 87, 4, 41, 87, 11, 50, 88, 21, 62, 79, 3, 57, 83, 14, 47, 84, 16, 50, 91, 9, 53, 83, 23, 58, 86, 4, 62, 87, 13])
f1score = np.array([71, 59, 6, 54, 62, 16, 60, 62, 32, 62, 60, 5, 64, 62, 22, 59, 65, 23, 64, 61, 15, 62, 54, 34, 66, 61, 8, 65, 69, 22])

c45_precision = np.mean(precisions)
c45_recall = np.mean(recalls)
c45_f1score = np.mean(f1score)


fig, ax = plt.subplots()
index = np.arange(4)
bar_width = 0.25

opacity = 0.4


# precisions = np.array([82, 47, 40, 88, 49, 60, 89, 47, 75, 68, 49, 25, 83, 51, 67, 89, 54, 20, 95, 46, 50, 73, 39, 83, 76, 48, 33, 79, 57, 67])
# recalls = np.array([59, 94, 8, 41, 92, 16, 44, 94, 25, 54, 90, 3, 54, 94, 10, 53, 88, 5, 50, 94, 9, 47, 90, 16, 61, 86, 4, 59, 97, 9])
# f1score = np.array([62, 69, 13, 56, 64, 25, 59, 63, 38, 60, 64, 6, 66, 66, 17, 67, 67, 8, 65, 62, 15, 57, 55, 27, 68, 62, 8, 68, 72, 15])

# pso1_precision = np.mean(precisions)
# pso1_recall = np.mean(recalls)
# pso1_f1score = np.mean(f1score)

# rects1 = ax.bar(index, [55.26, c45_precision, c45_recall, c45_f1score], bar_width,
#                 alpha=opacity, color='b',
#                 label='C4.5')

# rects2 = ax.bar(index + bar_width, [56.84, pso1_precision, pso1_recall, pso1_f1score], bar_width,
#                 alpha=opacity, color='r',
#                 label='PSO - C4.5')

# ax.set_ylabel('Nilai')
# ax.set_title('Nilai rata-rata tiap metrik pengukuran percobaan 1')
# ax.set_xticks(index + bar_width / 2)
# ax.set_yticks(np.linspace(0, 100, 11))
# ax.set_xticklabels(('Akurasi', 'Precision', 'Recall', 'F-Measure'))
# ax.legend()
# ax.grid()

# fig.tight_layout()
# plt.show()

# precisions = np.array([82, 47, 40, 88, 46, 60, 89, 38, 75, 68, 46, 25, 83, 49, 67, 89, 48, 60, 94, 45, 50, 73, 39, 83, 76, 48, 33, 84, 51, 80])
# recalls = np.array([59, 94, 8, 41, 95, 16, 44, 91, 25, 54, 90, 3, 54, 92, 10, 53, 95, 16, 42, 97, 9, 47, 90, 16, 61, 86, 4, 50, 92, 17])
# f1score = np.array([62, 69, 13, 56, 62, 25, 59, 54, 38, 60, 61, 6, 66, 63, 17, 67, 64, 25, 58, 61, 15, 57, 55, 27, 68, 62, 8, 63, 66, 29])

# pso2_precision = np.mean(precisions)
# pso2_recall = np.mean(recalls)
# pso2_f1score = np.mean(f1score)

# rects1 = ax.bar(index, [55.26, c45_precision, c45_recall, c45_f1score], bar_width,
#                 alpha=opacity, color='b',
#                 label='C4.5')

# rects2 = ax.bar(index + bar_width, [57.14, pso2_precision, pso2_recall, pso2_f1score], bar_width,
#                 alpha=opacity, color='r',
#                 label='PSO - C4.5')

# ax.set_ylabel('Nilai')
# ax.set_title('Nilai rata-rata tiap metrik pengukuran percobaan 2')
# ax.set_xticks(index + bar_width / 2)
# ax.set_yticks(np.linspace(0, 100, 11))
# ax.set_xticklabels(('Akurasi', 'Precision', 'Recall', 'F-Measure'))
# ax.legend()
# ax.grid()

# fig.tight_layout()
# plt.show()

precisions = np.array([82, 47, 40, 88, 49, 40, 89, 46, 75, 68, 49, 25, 79, 52, 67, 81, 52, 43, 95, 46, 50, 73, 39, 83, 76, 48, 33, 79, 57, 67])
recalls = np.array([59, 94, 8, 41, 92, 11, 44, 100, 25, 54, 90, 3, 51, 97, 10, 41, 86, 16, 50, 94, 9, 47, 90, 16, 61, 86, 4, 59, 97, 9])
f1score = np.array([62, 69, 13, 56, 64, 17, 59, 63, 38, 60, 64, 6, 62, 68, 17, 62, 68, 17, 65, 62, 15, 57, 55, 27, 68, 62, 8, 68, 72, 15])

pso3_precision = np.mean(precisions)
pso3_recall = np.mean(recalls)
pso3_f1score = np.mean(f1score)

rects1 = ax.bar(index, [55.26, c45_precision, c45_recall, c45_f1score], bar_width,
                alpha=opacity, color='b',
                label='C4.5')

rects2 = ax.bar(index + bar_width, [56.85, pso3_precision, pso3_recall, pso3_f1score], bar_width,
                alpha=opacity, color='r',
                label='PSO - C4.5')

ax.set_ylabel('Nilai')
ax.set_title('Nilai rata-rata tiap metrik pengukuran percobaan 3')
ax.set_xticks(index + bar_width / 2)
ax.set_yticks(np.linspace(0, 100, 11))
ax.set_xticklabels(('Akurasi', 'Precision', 'Recall', 'F-Measure'))
ax.legend()
ax.grid()

fig.tight_layout()
plt.show()