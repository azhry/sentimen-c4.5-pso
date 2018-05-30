from entities.Particle import Particle
import numpy as np
import random

class PSO_revision:

	def __init__(self, particleSize, populationSize, numIteration, c1, c2, target):
		self.particleSize = particleSize
		self.populationSize = populationSize
		self.numIteration = numIteration
		self.c1 = c1
		self.c2 = c2
		self.target = target
		self.particles = [Particle(self.particleSize) for _ in range(self.populationSize)]

	def exec(self, clf):
		r1, r2, r3 = [random.uniform(0, 1) for _ in range(3)]
		for _ in range(self.numIteration):
			for i in range(self.populationSize):
				self.particles[i].calculateBest(clf)

			self.particles = sorted(self.particles, key=lambda particle: particle.best, reverse=True)
			if self.particles[0].best >= self.target:
				return self.particles[0]
			
			for i in range(self.populationSize):
				self.particles[i].updateVelocity(self.c1, self.c2, r1, r2, self.particles[0].position)
				self.particles[i].updatePosition(r3)
		return self.particles[0]