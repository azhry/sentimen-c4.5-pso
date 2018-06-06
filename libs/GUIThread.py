from PyQt5.QtCore import QThread

class GUIThread(QThread):

	def __init__(self, clf, UI):
		QThread.__init__(self)
		self.clf = clf
		self.UI = UI

	def __del__(self):
		self.wait()

	def run(self):
		self.clf.constructTree(self.UI)