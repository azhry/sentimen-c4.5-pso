# from libs.PSO import PSO
# from libs.TFIDF import TFIDF
# from libs.C45 import C45
# from entities.Storage import Storage
# import matplotlib, numpy as np
# import matplotlib.pyplot as plt

# s = Storage()
# train = s.load("data/folds/train1.pckl")
# test = s.load("data/folds/test1.pckl")

# tfidf = TFIDF(train["Review"])
# tfidf.weights = tfidf.remove_zero_tfidf(tfidf.weights, 0.5)
# clf = C45(tfidf, train)
# clf.train()
# score = clf.score(tfidf, test)
# print(f"C4.5 score: {score}")

# particleSize = len(clf.termsInfo)
# popSize = 5
# iteration = 10
# c1, c2 = 0.5, 0.7
# target = score + 0.25
# pso = PSO(particleSize, popSize, iteration, c1, c2, target)
# pso.exec(train, test)

# x = len(pso.iterationBest)
# xAxis = [i for i in range(x)]
# fig, ax = plt.subplots()
# ax.plot(xAxis, pso.iterationBest)
# ax.plot(xAxis, [score for _ in range(x)])
# ax.set(xlabel="Iteration", ylabel="Particle Best", title="Particle Best Graph")
# plt.yticks(np.arange(score - 0.2, score + 0.2, 0.1))
# plt.show()

from entities.Particle import Particle
import matplotlib, numpy as np
import matplotlib.pyplot as plt

p = Particle(10)
loops = 150
lst = [p.tent_map() for _ in range(loops)]
fig, ax = plt.subplots()
ax.plot([i for i in range(loops)], lst)
ax.set(xlabel="Iteration", ylabel="Weight", title="Tent Mapping")
plt.yticks(np.arange(0.0, 1.0 + 0.1, 0.1))
plt.show()