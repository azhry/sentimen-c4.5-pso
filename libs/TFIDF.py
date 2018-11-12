from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

class TFIDF:
	"""
	Class yang digunakan untuk menangani proses TFIDF

	Attributes:
		count_vect (CountVectorizer): objek yang menangani proses tf
		tfidf_transformer (TfidfTransformer): objek yang menangni proses tfidf
		weights (2d-numpy): matrix hasil perhitungan tfidf
		termIndex (dict): dictionary term hasil tfidf
	"""

	def __init__(self, docs):
		"""
		Constructor
	
		Parameters:
		docs (list): daftar review yang jadi masukan untuk tfidf

		"""

		self.count_vect = CountVectorizer()
		self.tfidf_transformer = TfidfTransformer()
		self.weights = self.train_tfidf(docs)
		self.termIndex = self.count_vect.vocabulary_

	def train_tfidf(self, docs):
		"""
		Menghitung tfidf pada proses training

		parameters:
		docs (list): daftar review yang jadi masukan untuk tfidf

		Returns:
		2d-numpy: matrix hasil perhitungan tfidf

		"""

		train_counts = self.count_vect.fit_transform(docs).toarray()
		return self.tfidf_transformer.fit_transform(train_counts).toarray()

	def test_tfidf(self, docs):
		"""
		Menghitung tfidf pada proses testing

		parameters:
		docs (list): daftar review yang jadi masukan untuk tfidf

		Returns:
		2d-numpy: matrix hasil perhitungan tfidf

		"""

		test_counts = self.count_vect.transform(docs).toarray()
		return self.tfidf_transformer.transform(test_counts).toarray()

	def remove_zero_tfidf(self, xtr, min_tfidf=0.006):
		"""
		Filter term yang rata-rata tfidf-nya di bawah min_tfidf

		parameters:
		xtr (2d-numpy): matrix hasil perhitungan tfidf
		min_tfidf (double): nilai threshold untuk filter term

		Returns:
		xtr (2d-numpy): matrix hasil perhitungan tfidf yang telah di-filter

		"""

		# xtr = xtr.toarray()
		xtr[xtr < min_tfidf] = 0
		tfidf_means = np.mean(xtr, axis=0)
		deleted_idx = np.where(tfidf_means == 0)[0]
		self.termIndex = {key:val for key, val in self.termIndex.items() if val not in deleted_idx}
		# xtr = np.delete(xtr, deleted_idx, axis=1)
		return xtr