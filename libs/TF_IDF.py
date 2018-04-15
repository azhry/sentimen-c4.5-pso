from math import log

class TF_IDF():
    
    def __init__(self):
        self.weights = []
    
    def get_weight(self, term):
        pass
    
    def tf(self, term, document):
        return document.count(term) / float(len(document))
        
    def idf(self, term, documents):
        termCount = 0
        for doc in documents:
            if term in doc:
                termCount += 1
        
        if termCount > 0:
            return 1.0 + log(float(len(documents)) / termCount)
        else:
            return 1.0