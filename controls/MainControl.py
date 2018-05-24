from core.Database import Database
from libs.DataImporter import DataImporter
from libs.Preprocessor import Preprocessor
from helpers.Path import relative_path
from libs.C45_revision import C45_revision
from PyQt5.QtWidgets import *
import random
import numpy as np
import threading
# from PyQt5.QtCore import QThread, SIGNAL

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

	def foldData(self, k):
		self.k = k
		data = list(self.db.select("preprocessed_data"))
		random.shuffle(data)
		foldedData = np.array(np.array_split(data, k))
		for i, data in enumerate(foldedData):
			ids = ",".join([str(x) for x in data[:,0]])
			sql = "UPDATE preprocessed_data SET fold_number = " + str(i + 1) + " WHERE id IN (" + ids + ");"
			self.db.multiplesql(sql)
		return foldedData

	def trainModel(self):
		data = list(self.db.select("preprocessed_data"))
		clfs = []
		threads = []
		try:
			for i in range(self.k):
				# testData = list(filter(lambda row: row[3] == i + 1, data))
				# trainData = list(filter(lambda row: row[3] != i + 1, data))
				testData = []
				trainData = list(data)
				clfs.append(C45_revision(trainData, trainData, i + 1))
				threads.append(threading.Thread(target = clfs[i].optimize, args = ()))
				threads[i].start()
				print("Start thread: ", i)

			for i in range(self.k):
				threads[i].join()
		except:
			print("Error: unable to start thread")


	def readExcelFile(self):
		pass

	def classify(self):
		pass

	def delete_data(self):
		pass

	def show_data(self):
		pass