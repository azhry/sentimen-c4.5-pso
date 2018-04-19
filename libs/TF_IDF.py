from math import log
from helpers.Preprocessor import preprocess

class TF_IDF():
    
    def __init__(self, documents):
        self.weights = []
        self.terms = []
        self.idf = {}
        self.documents = documents

    def set_dictionary(self):
        self.terms = []
        for document in self.documents:
            self.terms = document[1].split(" ") + self.terms

    def get_dictionary(self):
        return self.terms

    def get_weight(self, term):
        return self.weights

    def set_weight(self, start = 0, end = None, thread_name = "Thread-X"):
        end = end or len(self.documents)
        for i in range(start, end):
            print("%s: calculate weights for document %d" % (thread_name, i + 1))
            weight = {}
            for term in self.terms:
                tf = self.tf(term, self.documents[i][1].split(" "))
                idf = self.idf[term]
                weight[term] = tf * idf
            self.weights.append(weight)
    
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

    # def idf(self, term):
    #     term_count = 0
    #     for doc in self.documents:
    #         if term in doc[1].split(" "):
    #             term_count += 1
        
    #     if term_count > 0:
    #         return 1.0 + log(float(len(self.documents)) / term_count)
    #     else:
    #         return 1.0

