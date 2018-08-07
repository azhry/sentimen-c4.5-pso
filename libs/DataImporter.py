import pandas as pd

class DataImporter():

	def __init__(self, filename):
		try:
			self.df = pd.read_excel(filename)
		except:
			self.df = None

	def get_data(self):
		return self.df
