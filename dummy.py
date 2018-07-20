# import pyximport; pyximport.install()
# from pyx.Particle import Particle
# from entities.Particle import Particle as P2
# import time, numpy as np, matplotlib.pyplot as plt

# start = time.time()
# p = Particle(10)
# for _ in range(100000):
# 	p.chaoticTentMap()

# end = time.time()

# start_2 = time.time()
# p = P2(10)
# for _ in range(100000):
# 	p.chaoticTentMap()

# end_2 = time.time()

# result = end - start
# result_2 = end_2 - start_2
# print(f"Cythonized particle executed in {round(result, 2)}s")
# print(f"Pure particle executed in {round(result_2, 2)}s")

# x_axis = ("Cython", "Python")
# y_axis = np.arange(len(x_axis))
# x_values = [round(result, 2), round(result_2, 2)]

# plt.bar(y_axis, x_values, align="center")
# plt.xticks(y_axis, x_axis)
# plt.ylabel("Time(s)")
# plt.title(f"Result = {int(result_2/result)}x speed improved")

# plt.show()

import numpy as np

def f(x):
	y = x
	if len(x) == 4:
		print("base case")
		return
	print(y)
	f([1, 2, 3, 4])
	print(y)

f(np.array([1, 2, 3]))