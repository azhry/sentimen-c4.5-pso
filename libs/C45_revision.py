from core.Database import Database
from libs.TFIDF_revision import TFIDF_revision
from math import log
import numpy as np

class C45_revision():

	def __init__(self, trainData, testData, foldNumber = 0):
		self.trainData 		= np.array(trainData)
		self.testData		= np.array(testData)
		self.termData		= {}
		self.foldNumber 	= foldNumber
		self.attributes 	= []
		self.db 			= Database("localhost", "root", "", "sentimen")

	def constructAttributes(self):
		for review in self.trainData[:,1]:
			attributes = review.split(" ")
			self.attributes.extend(attributes)

		self.attributes = set(self.attributes)
		for attribute in self.attributes:
			sql = "INSERT INTO attributes(attribute, active, fold_number) VALUES('" + attribute + "', 1, " + str(self.foldNumber) + ")"
			self.db.multiplesql(sql)

	def retrieveAttributes(self):
		# check if attributes are already constructed before
		if len(self.attributes) <= 0:
			attributes = self.db.select("attributes", "fold_number = " + str(self.foldNumber))
			for attr in attributes:
				self.attributes.append(attr[1])
		
		# otherwise construct new attributes
		else:
			self.constructAttributes()

	def calculateWeights(self):

		print("Calculating weights...")
		self.retrieveAttributes()

		tfidf = TFIDF_revision(self.trainData, self.attributes)
		tfidf.calculateTfIdf()
		tfidf.saveWeight(self.foldNumber)

	def calculateTotalEntropy(self):
		data = self.db.query("SELECT label, COUNT(id) AS total FROM preprocessed_data WHERE fold_number = " + str(self.foldNumber) + " GROUP BY label")
		length = 0
		for row in data:
			length += int(row[1])
		self.totalEntropy = 0
		for row in data:
			self.totalEntropy += (-1 * (row[1] / length) * log(row[1] / length, 10))

	def getDocumentsVector(self):
		print("Retrieving...")
		self.data = self.db.query("SELECT id_document, attribute, weight FROM weights WHERE fold_number = " + str(self.foldNumber))
		print("Retrieved")

	def getPossibleThresholds(self, attribute):
		# self.termData[attribute] = self.data[self.data[:,1] == attribute]
		possibleWeights = sorted(set([x[2] for x in self.data if x[1] == attribute]))
		possibleThresholds = []
		for i in range(len(possibleWeights) - 1):
			possibleThresholds.append((float(possibleWeights[i]) + float(possibleWeights[i + 1])) / 2)
		print("Weights %s %s: %s" % (self.foldNumber, attribute, possibleWeights))
		print("Thresholds %s %s: %s" % (self.foldNumber, attribute, possibleThresholds))

		# possible thresholds length <= 1 does not need to calculate information gain

	def getThresholdValue(self):
		self.retrieveAttributes()
		self.getDocumentsVector()
		print("Getting thresholds...")
		for attribute in self.attributes:
			self.getPossibleThresholds(attribute)