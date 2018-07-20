import MySQLdb
from pandas import DataFrame

class Database():

	def __init__(self, host, username, password, database):
		self.db = MySQLdb.connect(host, username, password, database)
		self.cursor = self.db.cursor()

	def insert_id(self):
		return self.cursor.lastrowid

	def select(self, table, condition = "", order = None):
		clen = len(condition)
		sql = "SELECT * FROM %s" % table
		if clen >= 3:
			sql += " WHERE %s " % condition
			if order is not None:
				sql += order
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except:
			print("Unable to fetch data")
			return None

	def select_pd(self, table, condition = "", order = None):
		clen = len(condition)
		sql = "SELECT * FROM %s" % table
		if clen >= 3:
			sql += " WHERE %s " % condition
			if order is not None:
				sql += order
		try:
			self.cursor.execute(sql)
			result = list(self.cursor.fetchall())
			df = DataFrame(result, columns = ["id", "Review", "Label", "fold_number"])
			return df
		except:
			print("Unable to fetch data")
			return None

	def query(self, sql):
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except:
			print("Unable to fetch data")
			return None

	def multiplesql(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

	def executeQuery(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

	def insert(self, table, data):
		dlen = len(data)
		sql = "INSERT INTO %s(" % table
		for i, key in enumerate(data.keys()):
			sql += key
			if i < dlen - 1:
				sql += ", "
		sql += ") VALUES("

		for i, value in enumerate(data.values()):
			sql += "'" + value + "'"
			if i < dlen - 1:
				sql += ", "
		sql += ")"

		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()


	def clean(self, table):
		sql = "TRUNCATE %s" % table
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

	def reset_auto_increment(self, table):
		sql = "ALTER TABLE %s AUTO_INCREMENT = 1" % table
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

	def close(self):
		self.db.close()

	def reset(self):
		self.clean("attributes")
		self.clean("preprocessed_data")
		self.clean("tree_nodes")
		self.clean("weights")