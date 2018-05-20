class Node():

	def __init__(self, attribute, threshold, nodeType = "attribute"):
		self.attribute = attribute
		self.threshold = threshold
		self.type = nodeType
		self.right = None
		self.left = None	

	def setRightChild(self, node):
		self.right = node

	def setLeftChild(self, node):
		self.left = node

	def getRightChild(self):
		return self.right

	def getLeftChild(self):
		return self.left

	def getNodeType(self):
		return self.type

	def getAttribute(self):
		return self.attribute

	def getThreshold(self):
		return self.threshold