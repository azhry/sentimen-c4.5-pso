class Node:

	def __init__(self, attribute, threshold, nodeType):
		self.attribute = attribute
		self.threshold = threshold
		self.nodeType = nodeType
		self.left = None
		self.right = None
		self.label = None

	def set_left_child(self, left):
		self.left = left

	def set_right_child(self, right):
		self.right = right

	def set_type(self, nodeType):
		self.nodeType = nodeType

	def set_label(self, label):
		self.label = label