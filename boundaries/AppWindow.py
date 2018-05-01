from PyQt5.QtWidgets import *
from controls.MainControl import MainControl
from core.Database import Database

class AppWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title 			= "Analisis Sentimen C4.5 - PSO"
		self.left			= 50
		self.top			= 50
		self.width			= 640
		self.height			= 480
		self.data 			= None
		self.mainControl 	= MainControl()
		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.tableWidget = QTableWidget(self)
		self.tableWidget.resize(490, 300)
		self.tableWidget.move(10, 30)
		
		self.preprocessButton = QPushButton("Preprocess", self)
		self.preprocessButton.move(520, 140)
		self.preprocessButton.clicked.connect(self.preprocessData)
		
		self.saveDataButton = QPushButton("Save Data", self)
		self.saveDataButton.move(520, 180)
		self.saveDataButton.clicked.connect(self.saveData)
	
		self.positiveLabelCount = QLabel("Positive: -", self)
		self.positiveLabelCount.move(10, 325)
		self.negativeLabelCount = QLabel("Negative: -", self)
		self.negativeLabelCount.move(150, 325)
		self.neutralLabelCount = QLabel("Neutral: -", self)
		self.neutralLabelCount.move(290, 325)

		# https://stackoverflow.com/questions/16568451/pyqt-how-to-make-a-textarea-to-write-messages-to-kinda-like-printing-to-a-co
		self.logOutput = QTextEdit(self)
		self.logOutput.setReadOnly(True)
		self.logOutput.resize(620, 90)
		self.logOutput.move(10, 380)

		self.renderMenuBar()
		self.show()

	def renderMenuBar(self):
		menuBar = self.menuBar()
		fileMenu = menuBar.addMenu("File")
		impMenu = QMenu("Import", self)
		impAct = QAction("Import Excel", self)
		impAct.triggered.connect(self.importExcel)
		impMenu.addAction(impAct)
		newAct = QAction("New", self)
		fileMenu.addAction(newAct)
		fileMenu.addMenu(impMenu)

	def saveData(self, data):
		print("Saved")

	def preprocessData(self, data):
		self.mainControl.preprocessData(self, data)

	def importExcel(self):
		self.data = self.mainControl.importExcel(self)
		if self.data is not None:
			self.renderTable(self.data)

	def renderTable(self, data):
		try:
			self.statusBar().showMessage("Importing....")
			self.tableWidget.setRowCount(len(data))
			self.tableWidget.setColumnCount(2)
			self.tableWidget.setHorizontalHeaderLabels(["Review", "Label"])
			tableHeader = self.tableWidget.horizontalHeader()
			tableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
			i = 0
			for review, label in zip(data["Review"], data["Label"]):
				self.tableWidget.setItem(i, 0, QTableWidgetItem(review))
				self.tableWidget.setItem(i, 1, QTableWidgetItem(label))
				i += 1
			self.tableWidget.show()
			self.statusBar().showMessage('Data imported')
		except:
			QMessageBox.question(self, "Error", "File tidak memiliki kolom Review dan Label")