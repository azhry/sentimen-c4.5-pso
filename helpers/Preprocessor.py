from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from helpers.Path import relative_path

def casefolding(str):
    return str.lower()
    
def tokenizing(str, delimiter = " "):
    return str.split(delimiter)
    
def stopword_removal(tokens):
    path = relative_path("id.stopwords.txt")
    with open(path) as f:
        stopwords = f.read().splitlines()
        return [token for token in tokens if token not in stopwords]
            
# stemming sekaligus casefolding
def stemming(str):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(str)
    
def preprocess(str):
    return stopword_removal(tokenizing(stemming(str)))