from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class Preprocessor():

	def __init__(self, stopword_path, correct_words_path):
		self.stopwords = StopWordRemoverFactory().get_stop_words()
		self.stemmer = StemmerFactory().create_stemmer()
		# self.specialCase = {
		# 	"dipesan": "pesan"
		# }

	# def casefolding(self, str):
	# 	return str.lower()

	def stemming(self, words):
		return self.stemmer.stem(words)

	def tokenizing(self, str, delimiter = " "):
		return str.split(delimiter)

	# def removing_stopwords(self, tokens):
	# 	return [token for token in tokens if token not in self.stopwords]

	def preprocess(self, words):
		return [token for token in self.tokenizing(self.stemming(words)) if token not in self.stopwords]
