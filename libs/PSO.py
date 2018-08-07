from entities.Particle import Particle
import random

class PSO:

	def __init__(self, particleSize, populationSize, numIteration, c1, c2, target):
		self.particleSize = particleSize
		self.populationSize = populationSize
		self.numIteration = numIteration
		self.c1 = c1
		self.c2 = c2
		self.target = target
		self.particles = [Particle(self.particleSize) for _ in range(self.populationSize)]
		self.iterationBest = []

	def exec(self, train, test):
		for _ in range(self.numIteration):
			for i in range(self.populationSize):
				print(self.particles[i].position)
				b = self.particles[i].calculate_best(train, test)
				print(f"Iter-{_} Particle-{i} best: {b}")
				self.particles[i].tent_map()

			self.particles = sorted(self.particles, key=lambda particle: particle.best, reverse=True)
			self.iterationBest.append(self.particles[0])
			print(f"Target: {self.target}")
			print(f"Iteration {_} best: {self.particles[0].best}")
			if self.particles[0].best > self.target:
				return self.particles[0]
			
			for i in range(self.populationSize):
				self.particles[i].update_velocity(self.c1, self.c2, self.particles[0].position)
				self.particles[i].update_position()
		self.iterationBest = sorted(self.iterationBest, key=lambda particle: particle.best, reverse=True)
		return self.iterationBest[0]