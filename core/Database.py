import pymysql

class Database():

	def __init__(self, host, username, password, database):
		self.db = pymysql.connect(host, username, password, database)
		self.cursor = self.db.cursor()

	def select(self, table, condition = ""):
		clen = len(condition)
		sql = "SELECT * FROM %s" % table
		if clen >= 3:
			sql += " WHERE %s" % condition
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except:
			print("Unable to fetch data")
			return None


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


	def update(self, table, data, condition):
		pass

	def delete(self, table, condition):
		pass

	def clean(self, table):
		sql = "DELETE FROM %s" % table
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()

	def close(self):
		self.db.close()