from core.Database import Database
from libs.DataImporter import DataImporter
from libs.Preprocessor import Preprocessor
from helpers.Path import relative_path
from PyQt5.QtWidgets import *
import random
import numpy as np
# from PyQt5.QtCore import QThread, SIGNAL

class MainControl():

	def __init__(self):
		self.db = Database("localhost", "root", "", "sentimen")
		self.stopwordPath = relative_path("id.stopwords.txt")
		self.correctWordsPath = relative_path("../libs/correct_words.json")
		self.preprocessor = Preprocessor(self.stopwordPath, self.correctWordsPath)


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
		data = list(self.db.select("preprocessed_data"))
		random.shuffle(data)
		foldedData = np.array(np.array_split(data, k))
		return foldedData

	def readExcelFile(self):
		pass

	def classify(self):
		pass

	def delete_data(self):
		pass

	def show_data(self):
		pass