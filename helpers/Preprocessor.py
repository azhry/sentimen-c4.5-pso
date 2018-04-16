from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from helpers.Path import relative_path

def casefolding(str):
    return str.lower()
    
def tokenizing(str, delimiter = " "):
    return str.split(delimiter)
    
def get_stopwords(path):
    with open(path) as f:
        return f.read().splitlines()

def stopword_removal(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]
            
# stemming sekaligus casefolding
def stemming(str):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(str)
    
def preprocess(str):
    stopwords = get_stopwords(relative_path("id.stopwords.txt"))
    return stopword_removal(tokenizing(stemming(str)), stopwords)