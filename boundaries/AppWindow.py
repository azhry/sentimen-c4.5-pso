from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from controls.MainControl import MainControl
from libs.TF_IDF import TF_IDF

class AppWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title 			= "Analisis Sentimen C4.5 - PSO"
		self.left			= 50
		self.top			= 50
		self.width			= 640
		self.height			= 580
		self.data 			= None
		self.mainControl 	= MainControl()
		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.renderMenuBar()
		self.renderTabs()
		
		self.tableWidget = QTableWidget(self.ETLTabs)
		self.tableWidget.resize(490, 300)
		self.tableWidget.move(10, 30)
		
		self.preprocessButton = QPushButton("Preprocess", self.ETLTabs)
		self.preprocessButton.move(520, 140)
		self.preprocessButton.clicked.connect(self.preprocessData)
		
		self.saveDataButton = QPushButton("Save Data", self.ETLTabs)
		self.saveDataButton.move(520, 180)
		self.saveDataButton.clicked.connect(self.saveData)
	
		self.positiveLabelCount = QLabel("Positive: -", self.ETLTabs)
		self.positiveLabelCount.move(10, 345)
		self.negativeLabelCount = QLabel("Negative: -", self.ETLTabs)
		self.negativeLabelCount.move(150, 345)
		self.neutralLabelCount = QLabel("Neutral: -", self.ETLTabs)
		self.neutralLabelCount.move(290, 345)

		self.renderTrainingTab()
		self.renderTestingTab()

		self.logOutput = QTextEdit(self)
		self.logOutput.setReadOnly(True)
		self.logOutput.resize(620, 90)
		self.logOutput.move(10, 460)
		self.logOutput.insertPlainText("Process log here..")
		self.logOutput.append("Process log #2")

		self.show()

	def renderTabs(self):
		self.tabs = QTabWidget(self)
		self.tabs.resize(620, 400)
		self.tabs.move(10, 20)

		self.ETLTabs = QWidget()
		self.trainTabs = QWidget()
		self.testTabs = QWidget()
		
		self.tabs.addTab(self.ETLTabs, "ETL")
		self.tabs.addTab(self.trainTabs, "Training")
		self.tabs.addTab(self.testTabs, "Testing")

	def renderETLTab(self):
		pass

	def renderTrainingTab(self):

		self.kFoldGroupBox = QGroupBox("k-Fold Cross Validation", self.trainTabs)
		self.kFoldGroupBox.move(450, 30)
		self.kFoldGroupBox.resize(150, 100)
		kFoldLayout = QFormLayout()
		kFoldValueTextbox = QLineEdit()
		kFoldValueTextbox.setText("10")
		kFoldLayout.addRow(QLabel("k"), kFoldValueTextbox)
		kFoldButton = QPushButton("Fold!")
		kFoldButton.clicked.connect(lambda: self.foldData(int(kFoldValueTextbox.text())))
		kFoldLayout.addRow(kFoldButton)
		self.kFoldGroupBox.setLayout(kFoldLayout)

		self.viewDataGroupBox = QGroupBox("View Data", self.trainTabs)
		self.viewDataGroupBox.move(450, 130)
		self.viewDataGroupBox.resize(150, 120)
		viewDataLayout = QFormLayout()
		kNumTextBox = QLineEdit()
		viewDataLayout.addRow(QLabel("k"), kNumTextBox)
		dataTypeComboBox = QComboBox()
		dataTypeComboBox.addItem("Training Data")
		dataTypeComboBox.addItem("Testing Data")
		viewDataLayout.addRow(QLabel("Type"), dataTypeComboBox)
		viewDataButton = QPushButton("View Data")
		viewDataLayout.addRow(viewDataButton)
		self.viewDataGroupBox.setLayout(viewDataLayout)

		self.trainC45GroupBox = QGroupBox("Train C4.5", self.trainTabs)
		self.trainC45GroupBox.move(450, 250)
		self.trainC45GroupBox.resize(150, 100)
		trainC45Layout = QFormLayout()
		trainC45Layout.addRow(QLabel("Total Entropy: "), QLabel("0"))
		trainC45Button = QPushButton("Train C4.5")
		trainC45Button.clicked.connect(self.trainModel)
		trainC45Layout.addRow(trainC45Button)
		self.trainC45GroupBox.setLayout(trainC45Layout)

		self.trainingTable = QTableWidget(self.trainTabs)
		self.trainingTable.resize(420, 300)
		self.trainingTable.move(10, 30)

	def renderTestingTab(self):
		self.testC45GroupBox = QGroupBox("Test C4.5", self.testTabs)
		testC45Layout = QFormLayout()
		testC45Button = QPushButton("Test C4.5")
		testC45Button.clicked.connect(self.testModel)
		testC45Layout.addRow(testC45Button)
		self.testC45GroupBox.setLayout(testC45Layout)
		self.testC45GroupBox.move(440, 30)

		self.attributeSelectionForm = QGroupBox("PSO Parameters", self.testTabs)
		self.attributeSelectionForm.move(440, 100)
		self.attributeSelectionForm.resize(150, 200)
		attributeSelectionLayout = QFormLayout()
		popSizeLabel, iterLabel, targetLabel, c1Label, c2Label = QLabel("Pop size"), QLabel("Iteration"), QLabel("Target(%)"), QLabel("C1"), QLabel("C2")
		c1Label.setToolTip("Penjelasan nilai convergence 1")
		c2Label.setToolTip("Penjelasan nilai convergence 2")
		popSizeTextBox, numIterationTextBox, targetTextBox, c1ValueTextBox, c2ValueTextBox = [QLineEdit() for _ in range(5)]
		c1ValueTextBox.setText("0.7")
		c2ValueTextBox.setText("0.5")
		attributeSelectionLayout.addRow(popSizeLabel, popSizeTextBox)
		attributeSelectionLayout.addRow(iterLabel, numIterationTextBox)
		attributeSelectionLayout.addRow(targetLabel, targetTextBox)
		attributeSelectionLayout.addRow(c1Label, c1ValueTextBox)
		attributeSelectionLayout.addRow(c2Label, c2ValueTextBox)
		optimizeC45Button = QPushButton("Optimize C4.5")

		optimizeC45Button.clicked.connect(lambda: self.optimizeModel(int(popSizeTextBox.text()), int(numIterationTextBox.text()), int(c1ValueTextBox.text()), int(c2ValueTextBox.text()), int(targetTextBox.text())))
		
		attributeSelectionLayout.addRow(optimizeC45Button)
		self.attributeSelectionForm.setLayout(attributeSelectionLayout)

		self.testingTable = QTableWidget(self.testTabs)
		self.testingTable.resize(420, 300)
		self.testingTable.move(10, 30)

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

	def foldData(self, k):
		self.mainControl.foldData(k)

	def saveData(self):
		self.mainControl.saveData()

	def trainModel(self):
		self.mainControl.trainModel()

	def testModel(self):
		self.mainControl.testModel()

	def optimizeModel(self, populationSize, numIteration, c1, c2, target):
		self.mainControl.optimizeModel(populationSize, numIteration, c1, c2, target)

	def preprocessData(self):
		try:
			self.mainControl.preprocessData(self, self.data)
		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setWindowTitle("Error")
			msg.setText("Anda harus mengimpor data terlebih dahulu")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()

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
			self.statusBar().showMessage("Data imported")
		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setWindowTitle("Error")
			msg.setText("File tidak memiliki kolom Review dan Label")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			self.statusBar().showMessage("Import failed")
