from core.Database import Database
from libs.DataImporter import DataImporter
from PyQt5.QtWidgets import *

class MainControl():

	def __init__(self):
		self.db = Database("localhost", "root", "", "sentimen")
		

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
		pass

	def readExcelFile(self):
		pass

	def classify(self):
		pass

	def delete_data(self):
		pass

	def show_data(self):
		pass