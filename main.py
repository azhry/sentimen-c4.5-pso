# # -*- coding: utf-8 -*-
import time
start_time = time.time()

import threading
from helpers.Path import relative_path
from libs.DataImporter import DataImporter
from libs.TF_IDF import TF_IDF
from libs.Preprocessor import Preprocessor
from libs.C45 import C45
from core.Database import Database

db = Database("localhost", "root", "", "sentimen")
# # db.clean("preprocessed_data")
# document_path = relative_path("../data/Formulir jajak pendapat bisnis dan pelayanan mengenai angkutan online (gojek, grab, dsb)(1-370).xlsx")
# # stopword_path = relative_path("id.stopwords.txt")
# # correct_words_path = relative_path("../libs/correct_words.json")

# importer = DataImporter(document_path)
# importer.count_labels()
# labels = importer.get_labels()
# data = importer.get_data()
# clf = C45(data, labels)
# print(clf.total_entropy())


# # documents = data.get_data()
# # print(db.select("preprocessed_data"))
# # preprocessor = Preprocessor(stopword_path, correct_words_path)
# # for document, label in zip(documents["Review"], documents["Label"]):
# # 	preprocessed = " ".join(preprocessor.preprocess(document))
# # 	db.insert("preprocessed_data", { "review": preprocessed, "label": label })
# # 	print(preprocessed)

documents = db.select("preprocessed_data")
tf_idf = TF_IDF(documents)
tf_idf.set_dictionary()
tf_idf.set_idf()
dictionary = tf_idf.get_dictionary()
print("Num attributes: %d" % len(dictionary))
try:
	t1 = threading.Thread(target=tf_idf.set_weight, args = (0, 185, "Thread-1"))
	t2 = threading.Thread(target=tf_idf.set_weight, args = (185, 370, "Thread-2"))
	# t3 = threading.Thread(target=tf_idf.set_weight, args = (148, 222, "Thread-3"))
	# t4 = threading.Thread(target=tf_idf.set_weight, args = (222, 296, "Thread-4"))
	# t5 = threading.Thread(target=tf_idf.set_weight, args = (296, 370, "Thread-5"))
	# t6 = threading.Thread(target=tf_idf.set_weight, args = (185, 222, "Thread-6"))
	# t7 = threading.Thread(target=tf_idf.set_weight, args = (222, 259, "Thread-7"))
	# t8 = threading.Thread(target=tf_idf.set_weight, args = (259, 296, "Thread-8"))
	# t9 = threading.Thread(target=tf_idf.set_weight, args = (296, 333, "Thread-9"))
	# t10 = threading.Thread(target=tf_idf.set_weight, args = (333, 370, "Thread-10"))

	t1.start()
	t2.start()
	# t3.start()
	# t4.start()
	# t5.start()
	# t6.start()
	# t7.start()
	# t8.start()
	# t9.start()
	# t10.start()
	
	# join the threads thus main thread will wait till this threads are done
	t1.join()
	t2.join()
	# t3.join()
	# t4.join()
	# t5.join()
	# t6.join()
	# t7.join()
	# t8.join()
	# t9.join()
	# t10.join()

except:
	print("Error: unable to start thread")


db.close()
print("\nExecuted in %.2f seconds" % (time.time() - start_time))

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot
 
# class App(QMainWindow):
 
#     def __init__(self):
#         super().__init__()
#         self.title 	= "Analisis Sentimen C4.5 - PSO"
#         self.left 	= 50
#         self.top 	= 50
#         self.width 	= 640
#         self.height = 480
#         self.initUI()
 
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         button = QPushButton("Classify", self)
#         button.setToolTip("This is an example button")
#         button.move(100, 70)
#         button.clicked.connect(self.classify)
#         self.textbox = QLineEdit(self)
#         self.textbox.move(100, 30)
#         self.textbox.resize(280, 20)
#         self.show()

#     @pyqtSlot()
#     def classify(self):
#     	self.statusBar().showMessage("Classifying...")
 
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

# import sys
# from boundaries.AppWindow import AppWindow
# from PyQt5.QtWidgets import QApplication

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = AppWindow()
#     sys.exit(app.exec_())