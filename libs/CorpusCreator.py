class CorpusCreator():
    
    def term_set(self, documents):
        dictionary = []
        for doc in documents:
            dictionary += doc
        return set(dictionary)