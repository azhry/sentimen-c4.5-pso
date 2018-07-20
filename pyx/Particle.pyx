import cython
cimport cython

import numpy as np
cimport numpy as np
import random, math
from libs.TFIDF import TFIDF

ctypedef np.float64_t float_t
ctypedef np.int32_t int_t

cdef class Particle:

	cdef public object position
	cdef object velocity
	cdef float_t best
	cdef float_t currBest
	cdef object currBestPosition
	cdef public float_t inertiaWeight

	def __cinit__(self, int size):
		self.position = np.array([random.choice((0, 1)) for _ in range(size)])
		self.velocity = np.array([random.uniform(0, 1) for _ in range(size)])
		self.best = 0
		self.currBest = 0
		self.currBestPosition = self.position
		self.inertiaWeight = random.uniform(0, 1)

	cpdef void updateVelocity(self, float_t c1, float_t c2, np.ndarray[int_t, ndim=1] particleBestPosition):
		self.velocity = np.array([self.calculateVelocity(v, c1, c2, px, pbx, x) for v, px, x, pbx in zip(self.velocity, self.position, self.currBestPosition, particleBestPosition)])

	cpdef void updatePosition(self):
		self.position = np.array([(1 if self.sigmoid(v) > random.uniform(0, 1) else 0) for v in self.velocity])

	cpdef float_t calculateVelocity(self, float_t v0, float_t c1, float_t c2, np.ndarray[int_t, ndim=1] px, np.ndarray[int_t, ndim=1] pbx, np.ndarray[int_t, ndim=1] x):
		return self.inertiaWeight * v0 + c1 * random.uniform(0, 1) * (px - pbx) + c2 * random.uniform(0, 1) * (px - x)

	cpdef float_t sigmoid(self, float_t v):
		if v < 0:
			return 1 - (1 / (1 + math.exp(-v)))
		return 1 / (1 + math.exp(-v))

	cpdef float_t calculateBest(self, clf):
		cdef np.ndarray[str, ndim=1] attributes = np.array(clf.attributes)[self.position.astype(bool)]
		tfidf = TFIDF(clf.trainData, attributes)
		tfidf.calculateIdf()
		clf.constructOptimizedTree(attributes)
		self.best = clf.evaluate(tfidf)
		return self.best

	cpdef public void chaoticTentMap(self):
		if self.inertiaWeight < 0.7:
			self.inertiaWeight = self.inertiaWeight / 0.7
		else:
			self.inertiaWeight = 10 / (3 * self.inertiaWeight * (1 - self.inertiaWeight))