from math import log
from helpers.Preprocessor import preprocess

class TF_IDF():
    
    def __init__(self, documents):
        self.weights = []
        self.terms = []
        self.documents = documents

    def set_dictionary(self):
        self.terms = []
        for document in self.documents:
            self.terms = preprocess(document) + self.terms
        print(self.terms)

    def get_dictionary(self):
        return self.terms

    def get_weight(self, term):
        return self.weights
    
    def tf(self, term, document):
        return document.count(term) / float(len(document))
        
    def idf(self, term):
        term_count = 0
        for doc in self.documents:
            if term in doc:
                term_count += 1
        
        if term_count > 0:
            return 1.0 + log(float(len(self.documents)) / term_count)
        else:
            return 1.0

