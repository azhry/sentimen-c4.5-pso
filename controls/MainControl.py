from core.Connection import Connection
from libs.DataImporter import DataImporter
# from libs.Preprocessor import Preprocessor
from pyx.Preprocessor import Preprocessor
from helpers.Path import relative_path
from libs.C45 import C45
from libs.TFIDF import TFIDF
from libs.Worker import Worker
from entities.Storage import Storage
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThreadPool, QEventLoop
from sklearn.model_selection import KFold
from sklearn import tree
import sys, time
import numpy as np, os

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
		self.storage = Storage()

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

	def preprocess_data(self, UI, data):
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

	def save_data(self, data):
		self.storage.save(data, "data/preprocessed/preprocessed.pckl")

	def fold_data(self, k, UI = None):
		self.k = k
		self.threadpool = QThreadPool()
		self.threadpool.setMaxThreadCount(self.k)
		self.data = self.storage.load("data/preprocessed/preprocessed.pckl")
		kf = KFold(n_splits=self.k, shuffle=True, random_state=2)
		for i, (train, test) in enumerate(kf.split(self.data)):
			self.storage.save(self.data.iloc[train], f"data/folds/train{i + 1}.pckl")
			self.storage.save(self.data.iloc[test], f"data/folds/test{i + 1}.pckl")
		if UI is not None:
			UI.logOutput.append(f"Data folded by {k}")

	def mltrain_fn(self, params={'i': None, 'remove_zero_tfidf': False, 'UI': None}):
		train = self.storage.load(f"data/folds/train{params['i'] + 1}.pckl")
		tfidf = TFIDF(train["Review"])
		if params['remove_zero_tfidf']:
			tfidf.weights = tfidf.remove_zero_tfidf(tfidf.weights, 0.5)
		clf = C45(tfidf, train)
		clf.train()
		return params["i"], clf, tfidf, params['UI'] or None

	def mltrain_result(self, res):
		self.attrs[res[0]] = res[2].count_vect.get_feature_names()
		self.clfs[res[0]] = res[1]
		self.tfidfs[res[0]] = res[2]
		self.storage.save(res[1], f"data/models/tree{res[0] + 1}.pckl")
		if res[3] is not None:
			res[3].logOutput.append(f"Tree {res[0] + 1} trained")


	def train_model(self, UI = None):
		self.attrs, self.clfs, self.tfidfs = ([0 for i in range(self.k)], [0 for i in range(self.k)], [0 for i in range(self.k)])
		el = QEventLoop()
		for i in range(self.k):
			if UI is not None:
				UI.logOutput.append(f"Train tree {i + 1}")
			params = {'i': i, 'remove_zero_tfidf': True, 'UI': UI}
			worker = Worker(self.mltrain_fn, params)
			worker.signals.result.connect(self.mltrain_result)
			self.threadpool.start(worker)

		self.threadpool.waitForDone()
		el.processEvents()
		el.exit()
		if UI is not None:
			UI.logOutput.append("Training completed")
		return self.attrs

	def test_model(self):
		scores = [0 for i in range(self.k)]
		for i in range(self.k):
			test = self.storage.load(f"data/folds/test{i + 1}.pckl")
			self.clfs[i].scores = self.clfs[i].score(self.tfidfs[i], test)
			scores[i] = self.clfs[i].scores
		return scores

	def optimizeModel(self, popSize, numIteration, c1, c2, target):
		results = []
		for i in range(self.k):
			results.append((self.clfs[i].foldNumber, self.clfs[i].optimize(popSize, numIteration, c1, c2, target)))
		return results

	def get_data(self, k, dstype):
		t = "train" if dstype == "Training Data" else "test"
		return self.storage.load(f"data/folds/{t}{k}.pckl")

	def resetDatabase(self):
		self.db.reset()

	def load_data(self, path):
		if os.path.exists(path):
			return self.storage.load(path)
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Error")
		msg.setText("Data yang dimuat tidak ada")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
		return None
