from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from controls.MainControl import MainControl
from core.Database import Database

class AppWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title 		= "Analisis Sentimen C4.5 - PSO"
		self.left		= 50
		self.top		= 50
		self.width		= 640
		self.height		= 480
		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		db = Database("localhost", "root", "", "sentimen")
		documents = db.select("preprocessed_data")

		self.tableWidget = QTableWidget(self)
		self.tableWidget.resize(490, 300)
		self.tableWidget.setRowCount(len(documents))
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(["Review", "Label"])
		tableHeader = self.tableWidget.horizontalHeader()
		tableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
		for i, document in enumerate(documents):
			self.tableWidget.setItem(i, 0, QTableWidgetItem(document[1]))
			self.tableWidget.setItem(i, 1, QTableWidgetItem(document[2]))
		self.tableWidget.move(10, 0)

		self.show()

