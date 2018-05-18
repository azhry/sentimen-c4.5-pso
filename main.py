# # -*- coding: utf-8 -*-
# import time
# start_time = time.time()

# import threading
# from helpers.Path import relative_path
# from libs.DataImporter import DataImporter
# from libs.TF_IDF import TF_IDF
# from libs.Preprocessor import Preprocessor
# from libs.C45 import C45
# from core.Database import Database

# db = Database("localhost", "root", "", "sentimen")
# document_path = relative_path("../data/Formulir jajak pendapat bisnis dan pelayanan mengenai angkutan online (gojek, grab, dsb)(1-370).xlsx")
# documents = db.select("preprocessed_data")
# # tf_idf = TF_IDF(documents, db)
# # tf_idf.set_dictionary()
# # tf_idf.clean_attributes()
# # tf_idf.set_attributes()
# # tf_idf.set_weights()
# # weights = tf_idf.get_weights()
# # for weight in weights:
# # 	id_document = weight["id_document"]
# # 	print("Saving document %d..." % id_document)
# # 	for t, w in weight["weight"].items():
# # 		print("%s: %f" % (t, w))
# # 		db.insert("weights", { "id_document": str(id_document), "attribute": t, "weight": str(w) })
# # attrs[np.logical_or.reduce([attrs[:,2] == x for x in ["efektif"]])]

# clf = C45(db)
# print(clf.discretize_attribute("gojek"))
import sys
from boundaries.AppWindow import AppWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec_())