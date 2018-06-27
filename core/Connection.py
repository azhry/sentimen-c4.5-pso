from core.Database import Database

class Connection:
	try:
		db = Database("localhost", "root", "", "sentimen_test")
	except:
		db = False

	def setConnection(host, username, password, database):
		return Database(host, username, password, database)