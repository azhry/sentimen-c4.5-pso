import numpy as np
import random
import math
from libs.TFIDF_revision import TFIDF_revision

class Particle:

	def __init__(self, size):
		self.position = np.array([random.choice((0, 1)) for _ in range(size)])
		self.velocity = np.array([0 for _ in range(size)])
		self.best = 0
		self.currBest = self.best
		self.currBestPosition = self.position

	def updateVelocity(self, c1, c2, r1, r2, particleBestPosition):
		self.velocity = np.array([self.calculateVelocity(v, c1, c2, r1, r2, px, pbx, x) for v, px, x in zip(self.velocity, self.position, self.currBestPosition, particleBestPosition)])

	def updatePosition(self, r3):
		self.position = np.array([(1 if self.sigmoid(v) > r3 else 0) for v in self.velocity])

	def calculateVelocity(self, v0, c1, c2, r1, r2, px, pbx, x):
		return v0 + c1 * r1 * (px - pbx) + c2 * r2 * (px - x)

	def sigmoid(self, v):
		return 1 / (1 + math.exp(-v))

	def calculateBest(self, clf):
		tfidf = TFIDF_revision(clf.trainData, clf.attributes[self.position.astype(bool)])
		tfidf.calculateIdf()
		return clf.evaluate(tfidf)