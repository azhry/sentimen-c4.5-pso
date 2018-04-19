from PyQt5.QtWidgets import QMainWindow
from controls.MainControl import MainControl

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
		self.show()

