from core.Connection import Connection
from libs.DataImporter import DataImporter
# from libs.Preprocessor import Preprocessor
from pyx.Preprocessor import Preprocessor
from helpers.Path import relative_path
from libs.C45 import C45
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random, sys, time
import numpy as np

class MainControl():

	def __init__(self, UI):
		self.db = Connection.db
		if not self.db:
			UI.msg = QMessageBox()
			UI.msg.setIcon(QMessageBox.Warning)
			UI.msg.setWindowTitle("Error")
			UI.msg.setText("Gagal koneksi ke basisdata")
			UI.msg.setStandardButtons(QMessageBox.Ok)
			UI.statusBar().showMessage("Database connection error")
			if UI.msg.exec_() == QMessageBox.Ok:
				sys.exit()

		self.stopwordPath = relative_path("id.stopwords.txt")
		self.correctWordsPath = relative_path("../libs/correct_words.json")
		self.preprocessor = Preprocessor(self.stopwordPath, self.correctWordsPath)
		self.k = 0

	def importExcel(self, UI):
		return self.openFileDialog(UI)

	def openFileDialog(self, UI):
		try:
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			fileName, _ = QFileDialog.getOpenFileName(UI, "Select Excel File", "", "Excel Files(*.xls *.xlsx)", options=options)
			if (fileName):
				importer = DataImporter(fileName)
				return importer.get_data()
		except:
			UI.msg = QMessageBox()
			UI.msg.setIcon(QMessageBox.Warning)
			UI.msg.setWindowTitle("Warning")
			UI.msg.setText("File tidak memiliki kolom Review dan Label")
			UI.msg.setStandardButtons(QMessageBox.Ok)
			UI.msg.show()
			UI.statusBar().showMessage("Import failed")
		return None

	def preprocessData(self, UI, data):
		self.preprocessedData = []
		totalTime = 0
		resultReview = []
		for i, (review, label) in enumerate(zip(data["Review"], data["Label"])):
			if i > 0:
				UI.tableWidget.item(i - 1, 0).setBackground(QColor(255, 255, 255))
			UI.tableWidget.item(i, 0).setBackground(QColor(255, 128, 128))
			startTime = time.time()	
			preprocessedReview = " ".join(self.preprocessor.preprocess(review))
			self.preprocessedData.append({ "review": preprocessedReview, "label" : label })
			endTime = time.time()
			resultReview.append(preprocessedReview)
			UI.logOutput.append(f"Review {i + 1} preprocessed in {round(endTime - startTime, 2)}s")
			totalTime += (endTime - startTime)
			UI.tableWidget.scrollToItem(UI.tableWidget.item(i - 1, 0), QAbstractItemView.PositionAtCenter)
			QApplication.processEvents()
		dlen = len(data)
		UI.tableWidget.item(dlen - 1, 0).setBackground(QColor(255, 255, 255))
		UI.tableWidget.scrollToItem(UI.tableWidget.item(dlen - 1, 0), QAbstractItemView.PositionAtCenter)
		UI.logOutput.append(f"{dlen} review(s) preprocessed in {round(totalTime, 2)}s")
		return resultReview

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
		self.data = list(self.db.select("preprocessed_data"))
		return foldedData

	def trainModel(self, UI = None):
		if self.data is None:
			self.data = list(self.db.select("preprocessed_data"))
		self.clfs = []
		try:
			for i in range(self.k):
				testData = list(filter(lambda row: row[3] == i + 1, self.data))
				trainData = list(filter(lambda row: row[3] != i + 1, self.data))
				self.clfs.append(C45(trainData, trainData, i + 1))
				self.clfs[i].constructTree(UI)
			
			if UI is not None:
				UI.logOutput.append("Training completed")
			return self.clfs
		except:
			print("Error training")

		return None

	def testModel(self):
		try:
			for i in range(self.k):
				print(f"Testing tree {i + 1}")
				self.clfs[i].accuracy = self.clfs[i].evaluate(self.clfs[i].tfidf)
				print(f"Accuracy of tree {i + 1}: {self.clfs[i].accuracy}%")
			return self.clfs
		except:
			print("Error testing")

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
				self.foldData(self.k)
			if dstype == "Training Data":
				return list(filter(lambda row: row[3] != kth, self.data))
			elif dstype == "Testing Data":
				return list(filter(lambda row: row[3] == kth, self.data))
			return None

	def resetDatabase(self):
		self.db.reset()

	def loadData(self):
		return self.db.select_pd("preprocessed_data")
