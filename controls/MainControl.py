from core.Database import Database
from libs.DataImporter import DataImporter
from libs.Preprocessor import Preprocessor
from helpers.Path import relative_path
from libs.C45_revision import C45_revision
from PyQt5.QtWidgets import *
import random
import numpy as np
import threading

class MainControl():

	def __init__(self):
		self.db = Database("localhost", "root", "", "sentimen_test")
		self.stopwordPath = relative_path("id.stopwords.txt")
		self.correctWordsPath = relative_path("../libs/correct_words.json")
		self.preprocessor = Preprocessor(self.stopwordPath, self.correctWordsPath)
		self.k = 0

	def importExcel(self, UI):
		return self.openFileDialog(UI)

	def openFileDialog(self, UI):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(UI, "Select Excel File", "", "Excel Files(*.xls *.xlsx)", options=options)
		if (fileName):
			importer = DataImporter(fileName)
			return importer.get_data()
		return None

	def preprocessData(self, UI, data):
		self.preprocessedData = []
		for review, label in zip(data["Review"], data["Label"]):
			preprocessedReview = " ".join(self.preprocessor.preprocess(review))
			self.preprocessedData.append({ "review": preprocessedReview, "label" : label })
			UI.logOutput.append(preprocessedReview)
			QApplication.processEvents()

	def saveData(self):
		sql = "INSERT INTO preprocessed_data(review, label) VALUES"
		for i, data in enumerate(self.preprocessedData):
			sql += "('" + data["review"] + "', '" + data["label"] + "')"
			if i < len(self.preprocessedData) - 1:
				sql += ","
		self.db.multiplesql(sql)

	def foldData(self, k, UI = None):
		self.k = k
		self.data = list(self.db.select("preprocessed_data"))
		random.shuffle(self.data)
		foldedData = np.array(np.array_split(self.data, k))
		for i, data in enumerate(foldedData):
			ids = ",".join([str(x) for x in data[:,0]])
			sql = "UPDATE preprocessed_data SET fold_number = " + str(i + 1) + " WHERE id IN (" + ids + ");"
			self.db.multiplesql(sql)
		if UI is not None:
			UI.logOutput.append(f"Data folded by {k}")
		return foldedData

	def trainModel(self, UI = None):
		if self.data is None:
			self.data = list(self.db.select("preprocessed_data"))
		self.clfs = []
		# threads = []
		try:
			for i in range(self.k):
				testData = list(filter(lambda row: row[3] == i + 1, self.data))
				trainData = list(filter(lambda row: row[3] != i + 1, self.data))
				self.clfs.append(C45_revision(trainData, trainData, i + 1))
				self.clfs[i].constructTree(UI)
				# threads.append(threading.Thread(target = self.clfs[i].constructTree, args = (UI,)))
				# threads[i].start()
			# 	print("Start thread: ", i)

			# for i in range(self.k):
			# 	threads[i].join()
			
			if UI is not None:
				UI.logOutput.append("Training completed")
			return self.clfs
		except:
			print("Error training: unable to start thread")

		return None

	def testModel(self):
		try:
			for i in range(self.k):
				print(f"Testing tree {i + 1}")
				self.clfs[i].accuracy = self.clfs[i].evaluate(self.clfs[i].tfidf)
				print(f"Accuracy of tree {i + 1}: {self.clfs[i].accuracy}%")
			return self.clfs
		except:
			print("Error testing: unable to start thread")

		return None

	def optimizeModel(self, popSize, numIteration, c1, c2, target):
		results = []
		for i in range(self.k):
			results.append((self.clfs[i].foldNumber, self.clfs[i].optimize(popSize, numIteration, c1, c2, target)))
		return results

	def getData(self, kth, dstype):
		if kth > self.k or kth <= 0:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setWindowTitle("Error")
			msg.setText("Anda harus memasukkan nilai k yang valid")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return None
		else:			
			if self.data is None:
				self.data = self.db.select("preprocessed_data")
			if dstype == "Training Data":
				return list(filter(lambda row: row[3] != kth, self.data))
			elif dstype == "Testing Data":
				return list(filter(lambda row: row[3] == kth, self.data))
			return None
