from math import exp
import random
import numpy as np

class PSO():
    
    def __init__(self, particleSize, populationSize, numIteration, c1, c2, target):
        self.populationSize = populationSize
        self.particleSize = particleSize
        self.numIteration = numIteration
        self.c1 = c1
        self.c2 = c2
        self.target = target

        self.r1, self.r2, self.r3 = [random.uniform(0, 1) for _ in range(3)]
        self.particles = self.initializePopulation()
        self.particles[:,2] = self.particles[:,0]
        self.previousBest = [0 for _ in range(self.populationSize)]
        self.particleBest = self.previousBest
        self.bestParticleIdx = None

    # first row: position(x)
    # second row: velocity(v)
    # third row: pBest(f)
    # note: pBest = previous best position
    def initializePopulation(self):
    	return np.array([[[random.choice((0, 1)) for _ in range(self.particleSize)], [0 for _ in range(self.particleSize)], [0 for _ in range(self.particleSize)]] for _ in range(self.populationSize)])

    # boolean indexing: arr[int_arr.astype(bool)]
    def searchBestSolution(self, clf):
    	attributes = np.array(clf.attributes)
    	for _ in range(self.numIteration):
    		for i, particle in enumerate(self.particles):
    			filteredAttributes = attributes[particle[0].astype(bool)]
    			particleBest = clf.buildTree(filteredAttributes)

    			if self.bestParticleIdx is None:
    				self.bestParticleIdx = i
    			else:
    				if particleBest > self.particleBest[self.bestParticleIdx]:
    					self.bestParticleIdx = i
    					self.particleBest[self.bestParticleIdx] = particleBest

    			self.particleBest[i] = particleBest

    		for i, particle in enumerate(self.particles):
    			self.particles[i] = self.updateParticle(particle)

    			if self.particleBest[i] > self.previousBest[i]:
    				self.previousBest[i] = self.particleBest[i]
    				self.particles[i][2] = self.particles[i][0]

    		print(self.particleBest)
    		if self.particleBest[self.bestParticleIdx] >= self.target:
    			break

    	print("End")
    	return self.particles[self.bestParticleIdx][0] # return the best particle position


    def calculateVelocity(self, x, v, f, d):
    	return v + self.c1 * self.r1 * (f - x) + self.c2 * self.r2 * (self.particles[self.bestParticleIdx][0][d] - x)

    def sigmoid(self, v):
    	return 1 / (1 + exp(-v))

    def updatePosition(self, v):
    	return 1 if self.sigmoid(v) > self.r3 else 0

    def updateParticle(self, particle):
    	newParticle = [[], [], []]
    	for i, x in enumerate(particle.T):
    		newVelocity = self.calculateVelocity(x[0], x[1], x[2], i)
    		newPosition = self.updatePosition(newVelocity)
    		newParticle[0].append(newPosition) 
    		newParticle[1].append(newVelocity)
    	newParticle[2] = particle[2]
    	return np.array(newParticle)

    def updateParticleVelocity(self, particle):
    	return np.array([[x[0], self.calculateVelocity(x[0], x[1], x[2], i), x[2]] for i, x in enumerate(particle.T)])

    def getPopulation(self):
    	return self.particles

    def updatePopulation(self, newPopulation):
    	self.particles = newPopulation