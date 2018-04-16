# -*- coding: utf-8 -*-
import time
start_time = time.time()

from helpers.Path import relative_path
from libs.DataImporter import DataImporter
from libs.TF_IDF import TF_IDF
from libs.Preprocessor import Preprocessor
from core.Database import Database

db = Database("localhost", "root", "", "sentimen")

document_path = relative_path("../data/Formulir jajak pendapat bisnis dan pelayanan mengenai angkutan online (gojek, grab, dsb)(1-370).xlsx")
stopword_path = relative_path("id.stopwords.txt")
correct_words_path = relative_path("../libs/correct_words.json")


# data = DataImporter(document_path)
# documents = data.get_data()
# print(db.select("preprocessed_data"))
preprocessor = Preprocessor(stopword_path, correct_words_path)
# for document, label in zip(documents["Review"], documents["Label"]):
# 	preprocessed = " ".join(preprocessor.preprocess(document))
# 	db.insert("preprocessed_data", { "review": preprocessed, "label": label })
# 	print(preprocessed)

# # tf_idf = TF_IDF(documents["Review"])
# tf_idf.set_dictionary()
# print(tf_idf.get_dictionary())



print("Executed in %s seconds" % (time.time() - start_time))