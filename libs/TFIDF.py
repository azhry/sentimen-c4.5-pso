from math import log
from core.Connection import Connection
from PyQt5.QtWidgets import QApplication

class TFIDF:

	def __init__(self, documents, terms):
		self.documents 	= documents
		self.db 	 	= Connection.db
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

	def calculateTfIdf(self, UI = None):
		self.calculateIdf()
		self.weights = []
		for i, document in enumerate(self.documents):
			if UI is not None:
				UI.logOutput.append(f"TFIDF-ing review {i + 1}")
				QApplication.processEvents()
			weight = {}
			for term in self.terms:
				weight[term] = self.tf(term, document[1]) * self.idf[term]
			self.weights.append({ "id_document": document[0], "weight": weight })
		return self.weights

	def saveWeight(self, foldNumber, UI = None):
		for i, weight in enumerate(self.weights):
			if UI is not None:
				UI.logOutput.append(f"Saving weights of review {i + 1}")
				QApplication.processEvents()
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
