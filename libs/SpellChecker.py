import re
from collections import Counter

class SpellChecker():

	def __init__(self, root_words_path):
		self.WORDS = Counter(self.words(open(root_words_path).read()))

	def words(self, text):
		return re.findall(r"\w+", text.lower())

	def P(self, word, N=sum(self.WORDS.values())):
		return self.WORDS[word] / N

	def correction(self, word):
		return max(self.candidates(word), key=self.P)

	def candidates(self, word):
		return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])