from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class Preprocessor:

	def __init__(self):
		self.stopwords = StopWordRemoverFactory().get_stop_words()
		self.stemmer = StemmerFactory().create_stemmer()

	def clean(self, words):
		return words.translate(str.maketrans("", "", ".,!?\"'#@%&/();:"))

	def stemming(self, words):
		return self.stemmer.stem(self.clean(words))

	def tokenizing(self, str, delimiter = " "):
		return str.split(delimiter)

	def preprocess(self, words):
		return [token for token in self.tokenizing(self.stemming(words)) if token not in self.stopwords]

	def selected_preprocess(self, words, selected_words):
		return [token for token in self.tokenizing(self.stemming(words)) if token not in self.stopwords and token in selected_words]