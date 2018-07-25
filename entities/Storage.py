import pickle, os, errno

class Storage:

	def save(self, obj, path):
		if not os.path.exists(os.path.dirname(path)):
			try:
				os.makedirs(os.path.dirname(path))
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise
		
		file = open(path, "wb")
		pickle.dump(obj, file)
		file.close()

	def load(self, path):
		file = open(path, "rb")
		obj = pickle.load(file)
		file.close()
		return obj