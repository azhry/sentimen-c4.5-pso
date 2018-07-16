import sys
from boundaries.AppWindow import AppWindow
from PyQt5.QtWidgets import QApplication

def run():
	app = QApplication(sys.argv)
	window = AppWindow()
	sys.exit(app.exec_())

if __name__ == "__main__":
	run()