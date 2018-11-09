import numpy as np, random, math
from libs.TFIDF import TFIDF
from libs.C45 import C45

class Particle:

	def __init__(self, size):
		self.position = np.array([random.choice((0, 1)) for _ in range(size)])
		self.velocity = np.array([random.uniform(0, 1) for _ in range(size)])
		self.best = 0
		self.currBest = 0
		self.currBestPosition = self.position
		self.inertiaWeight = random.uniform(0, 1)

	def update_velocity(self, c1, c2, particleBestPosition):
		self.velocity = np.array([self.calculate_velocity(v, c1, c2, px, pbx, x) for v, px, x, pbx in zip(self.velocity, self.position, self.currBestPosition, particleBestPosition)])

	def update_position(self):
		self.position = np.array([(1 if self.sigmoid(v) > random.uniform(0, 1) else 0) for v in self.velocity])

	def calculate_velocity(self, v0, c1, c2, px, pbx, x):
		return self.inertiaWeight * v0 + c1 * random.uniform(0, 1) * (px - pbx) + c2 * random.uniform(0, 1) * (px - x)

	def sigmoid(self, v):
		if v < 0:
			return 1 - (1 / (1 + math.exp(-v)))
		return 1 / (1 + math.exp(-v))

	def calculate_best(self, train, test):
		pos = self.position.astype(bool)
		tfidf = TFIDF(train["Review"])
		tfidf.weights = tfidf.remove_zero_tfidf(tfidf.weights, 0.5)
		tfidf.termIndex = {key:val for i, (key, val) in enumerate(tfidf.termIndex.items()) if pos[i] == True}
		print(f"Selected attributes: {len(tfidf.termIndex)}")
		self.clf = C45(tfidf, train)
		self.clf.train()
		self.best = self.clf.score(tfidf, test)
		return self.best

	def tent_map(self):
		if self.inertiaWeight < 0.7:
			self.inertiaWeight = self.inertiaWeight / 0.7
		else:
			self.inertiaWeight = (10 / 3) * (self.inertiaWeight * (1 - self.inertiaWeight))
		return self.inertiaWeight