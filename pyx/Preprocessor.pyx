from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

cdef class Preprocessor:

	cdef list stopwords
	cdef object stemmer 

	def __cinit__(self, str stopword_path, str correct_words_path):
		self.stopwords = StopWordRemoverFactory().get_stop_words()
		self.stemmer = StemmerFactory().create_stemmer()

	cpdef str stemming(self, str words):
		return self.stemmer.stem(words)

	cpdef list tokenizing(self, str words, str delimiter = " "):
		return words.split(delimiter)

	cpdef list preprocess(self, str words):
		return [token for token in self.tokenizing(self.stemming(words)) if token not in self.stopwords]
