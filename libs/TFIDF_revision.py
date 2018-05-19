from math import log
from core.Database import Database

class TFIDF_revision():

	def __init__(self, documents, terms):
		self.documents 	= documents
		self.db 	 	= Database("localhost", "root", "", "sentimen")
		self.terms		= terms
		self.idf 		= {}

	def tf(self, term, document):
		tokens = document.split(" ")
		return tokens.count(term) / float(len(tokens))

	def calculateIdf(self):
		dlen = len(self.documents)
		for term in self.terms:
			termCount = 0
			for document in self.documents:
				if term in document[1].split(" "):
					termCount += 1
			if termCount > 0:
				self.idf[term] = 1.0 + log(float(dlen) / termCount)
			else:
				self.idf[term] = 1.0

	def calculateTfIdf(self):
		self.calculateIdf()
		self.weights = []
		for document in self.documents:
			weight = {}
			for term in self.terms:
				weight[term] = self.tf(term, document[1]) * self.idf[term]
			self.weights.append({ "id_document": document[0], "weight": weight })
		return self.weights

	def saveWeight(self, foldNumber):
		print("Constructs query...")
		for weight in self.weights:
			sql = "INSERT INTO weights(id_document, attribute, weight, fold_number) VALUES"
			termWeight = weight["weight"].items()
			twlen = len(termWeight)
			j = 0
			for t, w in termWeight:
				sql += "(" + str(weight["id_document"]) + ", '" + t + "', " + str(w) + ", " + str(foldNumber) + ")"	
				if j < twlen - 1:
					sql += ","
				j += 1
			self.db.multiplesql(sql)
			print("Document %s saved." % (weight["id_document"]))
