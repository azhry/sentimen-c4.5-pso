from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json

class Preprocessor():

	def __init__(self, stopword_path, correct_words_path):
		with open(stopword_path) as f:
			self.stopwords = f.read().splitlines()
		factory = StemmerFactory()
		self.stemmer = factory.create_stemmer()

	def stemming(self, str):
		return self.stemmer.stem(str)

	def tokenizing(self, str, delimiter = " "):
		return str.split(delimiter)

	def removing_stopwords(self, tokens):
		return [token for token in tokens if token not in self.stopwords]

	def preprocess(self, str):
		return self.removing_stopwords(self.tokenizing(self.stemming(str)))