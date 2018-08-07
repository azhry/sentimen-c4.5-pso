from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from controls.MainControl import MainControl
import datetime, time
import matplotlib.pyplot as plt

class AppWindow(QMainWindow):

	def __init__(self, *args, **kwargs):
		super(AppWindow, self).__init__(*args, **kwargs)
		self.title 			= "Analisis Sentimen PSO - C4.5"
		self.left			= 50
		self.top			= 50
		self.width			= 640
		self.height			= 590
		self.data 			= None
		self.mainControl 	= MainControl(self)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.renderMenuBar()
		self.renderTabs()

		self.renderETLTab()
		self.renderTestingTab()

		self.logOutput = QTextEdit(self)
		self.logOutput.setReadOnly(True)
		self.logOutput.resize(620, 90)
		self.logOutput.move(10, 480)
		logDate = datetime.datetime.now().strftime("%I:%M %p, %d %B %Y")
		self.logOutput.insertPlainText(f"Log {logDate}")
		self.logOutput.textChanged.connect(lambda: self.clearTextEdit(self.logOutput))
		self.show()

	def renderTabs(self):
		self.tabs = QTabWidget(self)
		self.tabs.resize(620, 450)
		self.tabs.move(10, 20)

		self.ETLTabs = QWidget()
		self.testTabs = QWidget()
		
		self.tabs.addTab(self.ETLTabs, "Preprocess")
		self.tabs.addTab(self.testTabs, "Training - Testing")

	def renderETLTab(self):
		self.tableWidget = QTableWidget(self.ETLTabs)
		self.tableWidget.resize(420, 350)
		self.tableWidget.move(10, 30)

		# Preprocess button
		self.preprocessGroupBox = QGroupBox("Preprocess Data", self.ETLTabs)
		self.preprocessGroupBox.move(450, 30)
		self.preprocessGroupBox.resize(150, 70)
		preprocessLayout = QFormLayout()
		self.preprocessButton = QPushButton("Preprocess")
		self.preprocessButton.clicked.connect(self.preprocess_data)
		preprocessLayout.addRow(self.preprocessButton)
		self.preprocessGroupBox.setLayout(preprocessLayout)
		# Preprocess button (END)

		# k-Fold button
		self.kFoldGroupBox = QGroupBox("k-Fold Cross Validation", self.ETLTabs)
		self.kFoldGroupBox.move(450, 110)
		self.kFoldGroupBox.resize(150, 100)
		kFoldLayout = QFormLayout()
		kFoldValueTextbox = QLineEdit()
		kFoldValueTextbox.textChanged.connect(lambda: self.setLineEditDefaultNumber(kFoldValueTextbox, "2"))
		kFoldValueTextbox.setText("10")
		kFoldLayout.addRow(QLabel("k"), kFoldValueTextbox)
		kFoldButton = QPushButton("Fold!")
		kFoldButton.clicked.connect(lambda: self.fold_data(int(kFoldValueTextbox.text())))
		kFoldLayout.addRow(kFoldButton)
		self.kFoldGroupBox.setLayout(kFoldLayout)
		# k-Fold button (END)

		# View data layout
		self.viewDataGroupBox = QGroupBox("View Data", self.ETLTabs)
		self.viewDataGroupBox.move(450, 220)
		self.viewDataGroupBox.resize(150, 120)
		viewDataLayout = QFormLayout()
		kNumTextBox = QLineEdit()
		kNumTextBox.textChanged.connect(lambda: self.setLineEditDefaultNumber(kNumTextBox, "1"))
		kNumTextBox.setText("1")
		viewDataLayout.addRow(QLabel("k"), kNumTextBox)
		dataTypeComboBox = QComboBox()
		dataTypeComboBox.addItem("Training Data")
		dataTypeComboBox.addItem("Testing Data")
		viewDataLayout.addRow(QLabel("Type"), dataTypeComboBox)
		viewDataButton = QPushButton("View Data")
		viewDataButton.clicked.connect(lambda: self.view_data(int(kNumTextBox.text()), dataTypeComboBox.currentText()))
		viewDataLayout.addRow(viewDataButton)
		self.viewDataGroupBox.setLayout(viewDataLayout)
		# View data layout (END)

	def renderTestingTab(self):
		self.testC45GroupBox = QGroupBox("Train and Test C4.5", self.testTabs)
		testC45Layout = QFormLayout()
		testC45Button = QPushButton("Train and Test")
		testC45Button.clicked.connect(self.train_and_test)
		testC45Layout.addRow(testC45Button)
		self.testC45GroupBox.setLayout(testC45Layout)
		self.testC45GroupBox.resize(150, 70)
		self.testC45GroupBox.move(440, 30)

		self.attributeSelectionForm = QGroupBox("PSO Parameters", self.testTabs)
		self.attributeSelectionForm.move(440, 100)
		self.attributeSelectionForm.resize(150, 200)
		attributeSelectionLayout = QFormLayout()
		popSizeLabel, iterLabel, targetLabel, c1Label, c2Label = QLabel("Pop size"), QLabel("Iteration"), QLabel("Target(+%)"), QLabel("C1"), QLabel("C2")
		c1Label.setToolTip("Penjelasan nilai convergence 1")
		c2Label.setToolTip("Penjelasan nilai convergence 2")
		popSizeTextBox, numIterationTextBox, targetTextBox, c1ValueTextBox, c2ValueTextBox = [QLineEdit() for _ in range(5)]
		c1ValueTextBox.setText("0.7")
		c2ValueTextBox.setText("0.5")
		targetTextBox.setText("0")
		attributeSelectionLayout.addRow(popSizeLabel, popSizeTextBox)
		attributeSelectionLayout.addRow(iterLabel, numIterationTextBox)
		attributeSelectionLayout.addRow(targetLabel, targetTextBox)
		attributeSelectionLayout.addRow(c1Label, c1ValueTextBox)
		attributeSelectionLayout.addRow(c2Label, c2ValueTextBox)
		optimizeC45Button = QPushButton("Optimize C4.5")

		optimizeC45Button.clicked.connect(lambda: self.optimize_model(int(popSizeTextBox.text()), int(numIterationTextBox.text()), float(c1ValueTextBox.text()), float(c2ValueTextBox.text()), int(targetTextBox.text())))
		
		attributeSelectionLayout.addRow(optimizeC45Button)
		self.attributeSelectionForm.setLayout(attributeSelectionLayout)

		self.testingTable = QTableWidget(self.testTabs)
		self.testingTable.resize(420, 300)
		self.testingTable.move(10, 30)

	def renderMenuBar(self):
		menuBar = self.menuBar()
		self.fileMenu = menuBar.addMenu("File")
		self.importExcelMenu = QAction("Import Excel", self)
		self.importExcelMenu.triggered.connect(self.import_excel)
		self.fileMenu.addAction(self.importExcelMenu)
		self.loadDataMenu = QAction("Load Data", self)
		self.loadDataMenu.triggered.connect(self.load_data)
		self.fileMenu.addAction(self.loadDataMenu)

	def fold_data(self, k):
		try:
			self.mainControl.fold_data(k, self)
			self.testingTable.setRowCount(k)
			self.testingTable.setColumnCount(4)
			self.testingTable.setHorizontalHeaderLabels(["Attrs", "C4.5", "PSO - C4.5", "Removed Attrs"])
			tableHeader = self.testingTable.horizontalHeader()
			tableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
		except:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setText("Anda harus mengimpor data terlebih dahulu")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()

	def load_data(self):
		self.data = self.mainControl.load_data("data/preprocessed/preprocessed.pckl")
		self.renderTable(self.data)

	def save_data(self, data):
		self.mainControl.save_data(data)

	def train_model(self):
		attrs = self.mainControl.train_model(self)
		if attrs is not None:
			for i, attr in enumerate(attrs):
				self.testingTable.setItem(i, 0, QTableWidgetItem(f"{len(attr)}"))

	def train_and_test(self):
		self.train_model()
		self.test_model()

		self.optimize_model(20, 40, 0.7, 0.2, 10)

	def test_model(self):
		self.scores = self.mainControl.test_model()
		if self.scores is not None:
			for i, score in enumerate(self.scores):
				self.testingTable.setItem(i, 1, QTableWidgetItem(f"{round(score * 100, 2)}%"))
		else:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setText("Testing: anda harus melatih algoritma C4.5 terlebih dahulu")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()

	def optimize_model(self, popSize, numIteration, c1, c2, target = 0):
		try:
			self.results = self.mainControl.optimize_model(popSize, numIteration, c1, c2, target / 100)
			for i, result in enumerate(self.results):
				self.testingTable.setItem(i, 2, QTableWidgetItem(f"{round(result.best * 100, 2)}%"))
				self.testingTable.setItem(i, 3, QTableWidgetItem(f"{list(result.position).count(0)}"))
		except:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setText("Testing: anda harus memasukkan nilai parameter PSO")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()

	def view_data(self, kth, dstype):
		try:
			data = self.mainControl.get_data(kth, dstype)
			self.tableWidget.setRowCount(len(data))
			self.tableWidget.setColumnCount(2)
			self.tableWidget.setHorizontalHeaderLabels(["Review", "Label"])
			tableHeader = self.tableWidget.horizontalHeader()
			tableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
			for i, (review, label) in enumerate(zip(data["Review"], data["Label"])):
				self.tableWidget.setItem(i, 0, QTableWidgetItem(review))
				self.tableWidget.setItem(i, 1, QTableWidgetItem(label))
			self.tableWidget.show()
		except:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setText("Anda harus menentukan nilai k yang ingin dilihat")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()

	def preprocess_data(self):
		try:
			if self.data is None:
				raise Exception("Anda harus mengimpor data terlebih dahulu")
			self.data["Review"] = self.mainControl.preprocess_data(self, self.data)
			self.save_data(self.data)
		except:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setText("Anda harus mengimpor data terlebih dahulu")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()

	def import_excel(self):
		self.data = self.mainControl.import_excel(self)
		if self.data is not None:
			self.renderTable(self.data)
		self.logOutput.append("Data imported")

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
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setText("File tidak memiliki kolom Review dan Label")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()
			self.statusBar().showMessage("Import failed")

	def setLineEditDefaultNumber(self, lineEdit, defaultNumber):
		if lineEdit.text() == "":
			lineEdit.setText(f"{defaultNumber}")

	def clearTextEdit(self, textEdit):
		if textEdit.document().blockCount() > 500:
			textEdit.clear()