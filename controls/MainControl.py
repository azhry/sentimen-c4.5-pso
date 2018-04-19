from core.Database import Database

class MainControl():

	def __init__(self):
		self.db = Database("localhost", "root", "", "sentimen")
		

	def import_data(self):
		pass

	def classify(self):
		pass

	def delete_data(self):
		pass

	def show_data(self):
		pass