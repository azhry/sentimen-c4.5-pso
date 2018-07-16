import numpy as np
import random, math
from libs.TFIDF import TFIDF

class Particle:

	def __init__(self, size):
		self.position = np.array([random.choice((0, 1)) for _ in range(size)])
		self.velocity = np.array([random.uniform(0, 1) for _ in range(size)])
		self.best = 0
		self.currBest = 0
		self.currBestPosition = self.position
		self.inertiaWeight = random.uniform(0, 1)

	def updateVelocity(self, c1, c2, particleBestPosition):
		self.velocity = np.array([self.calculateVelocity(v, c1, c2, px, pbx, x) for v, px, x, pbx in zip(self.velocity, self.position, self.currBestPosition, particleBestPosition)])

	def updatePosition(self):
		self.position = np.array([(1 if self.sigmoid(v) > random.uniform(0, 1) else 0) for v in self.velocity])

	def calculateVelocity(self, v0, c1, c2, px, pbx, x):
		return self.inertiaWeight * v0 + c1 * random.uniform(0, 1) * (px - pbx) + c2 * random.uniform(0, 1) * (px - x)

	def sigmoid(self, v):
		if v < 0:
			return 1 - (1 / (1 + math.exp(-v)))
		return 1 / (1 + math.exp(-v))

	def calculateBest(self, clf):
		attributes = np.array(clf.attributes)[self.position.astype(bool)]
		tfidf = TFIDF(clf.trainData, attributes)
		tfidf.calculateIdf()
		clf.constructOptimizedTree(attributes)
		self.best = clf.evaluate(tfidf)
		return self.best

	def chaoticTentMap(self):
		if self.inertiaWeight < 0.7:
			self.inertiaWeight = self.inertiaWeight / 0.7
		else:
			self.inertiaWeight = 10 / (3 * self.inertiaWeight * (1 - self.inertiaWeight))