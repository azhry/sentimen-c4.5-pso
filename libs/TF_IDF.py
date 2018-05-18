from math import log
from helpers.Preprocessor import preprocess

class TF_IDF():
    
    def __init__(self, documents, db):
        self.weights = []
        self.terms = []
        self.attributes = db.select("attributes")
        self.idf = {}
        self.documents = documents
        self.db = db

    def set_dictionary(self):
        self.terms = []
        for document in self.documents:
            self.terms = document[1].split(" ") + self.terms
        self.terms = list(set(self.terms))

    def set_attributes(self):
        for attr in self.terms:
            self.db.insert("attributes", { "attribute": attr })
        self.attributes = self.db.select("attributes")

    def clean_attributes(self):
        self.db.clean("attributes")
        self.db.reset_auto_increment("attributes")

    def get_dictionary(self):
        return self.terms

    def get_weights(self):
        return self.weights

    def set_weights(self, start = 0, end = None, thread_name = "Thread-X", UI = None):
        end = end or len(self.documents)
        self.set_idf()
        for i in range(start, end):
            print("%s: calculate weights for document %d" % (thread_name, i + 1))
            if UI is not None:
                UI.logOutput.append("%s: calculate weights for document %d" % (thread_name, i + 1))
            weight = {}
            for attr in self.attributes:
                tf = self.tf(attr[1], self.documents[i][1].split(" "))
                idf = self.idf[attr[1]]
                weight[attr[1]] = tf * idf
            self.weights.append({ "id_document": self.documents[i][0], "weight": weight })

    def clean_weights(self, db):
        db.clean("weights")
        db.reset_auto_increment("weights")

    def tf(self, term, document):
        return document.count(term) / float(len(document))
        
    def set_idf(self):
        dlen = len(self.documents)
        if len(self.terms) <= 0:
            self.set_dictionary()
        for term in self.terms:
            term_count = 0
            for doc in self.documents:
                if term in doc[1].split(" "):
                    term_count += 1
            if term_count > 0:
                self.idf[term] = 1.0 + log(float(dlen) / term_count)
            else:
                self.idf[term] = 1.0