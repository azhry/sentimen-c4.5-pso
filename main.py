# # -*- coding: utf-8 -*-
# import time
# start_time = time.time()

# import threading
# from helpers.Path import relative_path
# from libs.DataImporter import DataImporter
# from libs.TF_IDF import TF_IDF
# from libs.Preprocessor import Preprocessor
# from core.Database import Database

# db = Database("localhost", "root", "", "sentimen")
# # db.clean("preprocessed_data")
# # document_path = relative_path("../data/Formulir jajak pendapat bisnis dan pelayanan mengenai angkutan online (gojek, grab, dsb)(1-370).xlsx")
# # stopword_path = relative_path("id.stopwords.txt")
# # correct_words_path = relative_path("../libs/correct_words.json")


# # data = DataImporter(document_path)
# # documents = data.get_data()
# # print(db.select("preprocessed_data"))
# # preprocessor = Preprocessor(stopword_path, correct_words_path)
# # for document, label in zip(documents["Review"], documents["Label"]):
# # 	preprocessed = " ".join(preprocessor.preprocess(document))
# # 	db.insert("preprocessed_data", { "review": preprocessed, "label": label })
# # 	print(preprocessed)

# documents = db.select("preprocessed_data")
# tf_idf = TF_IDF(documents)
# tf_idf.set_dictionary()
# dictionary = tf_idf.get_dictionary()
# print("Num attributes: %d" % len(dictionary))
# try:
# 	threading.Thread(target=tf_idf.set_weight, args = (0, 37, "Thread-1")).start()
# 	threading.Thread(target=tf_idf.set_weight, args = (37, 74, "Thread-2")).start()
# 	threading.Thread(target=tf_idf.set_weight, args = (74, 111, "Thread-3")).start()
# 	threading.Thread(target=tf_idf.set_weight, args = (111, 148, "Thread-4")).start()
# 	threading.Thread(target=tf_idf.set_weight, args = (148, 185, "Thread-5")).start()
# 	# threading.Thread(target=tf_idf.set_weight, args = (185, 222, "Thread-6")).start()
# 	# threading.Thread(target=tf_idf.set_weight, args = (222, 259, "Thread-7")).start()
# 	# threading.Thread(target=tf_idf.set_weight, args = (259, 296, "Thread-8")).start()
# 	# threading.Thread(target=tf_idf.set_weight, args = (296, 333, "Thread-9")).start()
# 	# threading.Thread(target=tf_idf.set_weight, args = (333, 370, "Thread-10")).start()
# except:
# 	print("Error: unable to start thread")


# db.close()
# # print("\nExecuted in %.2f seconds" % (time.time() - start_time))

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title 	= "Analisis Sentimen C4.5 - PSO"
        self.left 	= 50
        self.top 	= 50
        self.width 	= 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        button = QPushButton("Classify", self)
        button.setToolTip("This is an example button")
        button.move(100, 70)
        button.clicked.connect(self.classify)
        self.textbox = QLineEdit(self)
        self.textbox.move(100, 30)
        self.textbox.resize(280, 20)
        self.show()

    @pyqtSlot()
    def classify(self):
    	self.statusBar().showMessage("Classifying...")
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())