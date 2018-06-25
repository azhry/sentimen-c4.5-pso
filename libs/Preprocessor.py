from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json

class Preprocessor():

	def __init__(self, stopword_path, correct_words_path):
		with open(stopword_path) as f:
			self.stopwords = f.read().splitlines()
		factory = StemmerFactory()
		self.stemmer = factory.create_stemmer()
		self.specialCase = {
			"dipesan": "pesan"
		}

	def casefolding(self, str):
		return str.lower()

	def stemming(self, word):
		return self.stemmer.stem_word(word)

	def tokenizing(self, str, delimiter = " "):
		return str.split(delimiter)

	def removing_stopwords(self, tokens):
		return [token for token in tokens if token not in self.stopwords]

	def preprocess(self, str):
		return self.removing_stopwords([self.stemming(word) if word not in self.specialCase else self.specialCase[word] for word in self.tokenizing(self.casefolding(str))])