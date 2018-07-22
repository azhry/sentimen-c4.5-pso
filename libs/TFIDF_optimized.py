from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.feature_selection import mutual_info_classif
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import operator

class TFIDF_optimized:

	def __init__(self, documents):
		self.documents 	= documents
		self.stopwords  = StopWordRemoverFactory().get_stop_words()
		self.tfidf_vectorizer = TfidfVectorizer(max_df=0.9, 
			min_df=1, 
			lowercase=True, 
			stop_words=self.stopwords)
		self.weights = self.tfidf()
		self.termIndex = self.tfidf_vectorizer.vocabulary_

	def tfidf(self):
		return self.tfidf_vectorizer.fit_transform(self.documents).toarray()

	def terms_info(self):
		return self.tfidf_vectorizer.vocabulary_

	def term_weights(self, term):
		return self.weights[:, self.termIndex[term]]
