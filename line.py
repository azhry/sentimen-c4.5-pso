import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def get_data(data, start):
	x = []
	for i in range(start, len(data), 3):
		x.append(data[i])
	return x

precisions = np.array([82, 47, 40, 88, 49, 60, 89, 47, 75, 68, 49, 25, 83, 51, 67, 89, 54, 20, 95, 46, 50, 73, 39, 83, 76, 48, 33, 79, 57, 67])
recalls = np.array([59, 94, 8, 41, 92, 16, 44, 94, 25, 54, 90, 3, 54, 94, 10, 53, 88, 5, 50, 94, 9, 47, 90, 16, 61, 86, 4, 59, 97, 9])
f1score = np.array([62, 69, 13, 56, 64, 25, 59, 63, 38, 60, 64, 6, 66, 66, 17, 67, 67, 8, 65, 62, 15, 57, 55, 27, 68, 62, 8, 68, 72, 15])

c45_precision = np.mean(precisions)
c45_recall = np.mean(recalls)
c45_f1score = np.mean(f1score)


fig, ax = plt.subplots()
index = np.arange(4)
bar_width = 0.25

opacity = 0.4

f_pos = get_data(f1score, 0)
f_neg = get_data(f1score, 1)
f_net = get_data(f1score, 2)


x_axis = np.linspace(0, 10, 10)
y_axis = [55.26 - 15, 55.26, 55.26 + 15]
plt.plot(x_axis, f_pos, label="F-Measure Positif")
plt.scatter(x_axis, f_pos)
plt.plot(x_axis, f_neg, label="F-Measure Negatif")
plt.scatter(x_axis, f_neg)
plt.plot(x_axis, f_net, label="F-Measure Netral")
plt.scatter(x_axis, f_net)
plt.title(f"Perbandingan F-Measure Tiap Label Percobaan 1")
plt.grid()
plt.legend()
plt.xlabel("k")
plt.ylabel("Nilai(%)")
plt.yticks(y_axis)
plt.show()