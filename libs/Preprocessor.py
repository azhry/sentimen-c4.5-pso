from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class Preprocessor():

	def __init__(self):
		self.stopwords = StopWordRemoverFactory().get_stop_words()
		self.stemmer = StemmerFactory().create_stemmer()

	def stemming(self, words):
		return self.stemmer.stem(words)

	def tokenizing(self, str, delimiter = " "):
		return str.split(delimiter)

	def preprocess(self, words):
		return [token for token in self.tokenizing(self.stemming(words)) if token not in self.stopwords]
