from math import log
from collections import Counter
from entities.Node import Node
from libs.TFIDF_optimized import TFIDF_optimized
import numpy as np

class C45_optimized:

	def __init__(self, vectors, data):
		self.vectors = vectors
		self.data = data
		self.npdata = data.as_matrix()
		self.totalEntropy = 0
		self.weights = self.vectors.weights
		self.termsInfo = self.vectors.termIndex
		self.attributes = np.array(list(self.termsInfo.keys()))
		print(self.attributes)
		self.tree = None

	def calculate_total_entropy(self):
		self.totalEntropy = 0
		labelCount = Counter(self.data["Label"])
		labelValue = list(labelCount.values())
		labelTotal = sum(labelValue)
		for value in labelValue:
			self.totalEntropy += (-1 * (value / labelTotal) * log(value / labelTotal, 10))

	def calculate_attribute_gain(self, attribute, threshold, excludedRows = ()):
		leftChild, rightChild = self.get_child_nodes(attribute, threshold, excludedRows)
		left = self.npdata[list(leftChild)]
		right = self.npdata[list(rightChild)]
		leftEntropy, leftTotal = self.calculate_entropy(left)
		rightEntropy, rightTotal = self.calculate_entropy(right)
		total = leftTotal + rightTotal
		info = (leftTotal / total) * leftEntropy + (rightTotal / total) * rightEntropy if total != 0 else 0
		return self.totalEntropy - info

	def calculate_entropy(self, data):
		labelCount = Counter(data[:, -2])
		labelValue = list(labelCount.values())
		labelTotal = sum(labelValue)
		entropy = sum(-1 * ((x / labelTotal) * (log(x / labelTotal, 10) if (x / labelTotal) != 0 else 0)) for x in labelValue) if labelTotal != 0 else 0
		return entropy, labelTotal

	def get_possible_thresholds(self, attribute, excludedRows = ()):
		vectors = np.delete(self.weights, excludedRows, axis = 0)
		weights = vectors[:, self.termsInfo[attribute]]
		weights = sorted(set(weights))
		weightCount = len(weights)
		thresholds = []
		for i in range(weightCount - 1):
			thresholds.append((float(weights[i]) + float(weights[i + 1])) / 2)
		return thresholds

	def pruning(self, excludedRows = ()):
		attrThresholds = []
		for attr in self.attributes:
			thresholds = self.get_possible_thresholds(attr, excludedRows)
			if len(thresholds) <= 0:
				continue
			thresholdGain = []
			for threshold in thresholds:
				gain = self.calculate_attribute_gain(attr, threshold, excludedRows)
				thresholdGain.append([threshold, gain])
			thresholdGain = sorted(thresholdGain, key = lambda x: x[1], reverse = True)
			attrThreshold = [attr]
			attrThreshold.extend(thresholdGain[0])
			attrThresholds.append(attrThreshold)
		return sorted(attrThresholds, key = lambda x: x[2], reverse = True)

	def get_child_nodes(self, attribute, threshold, excludedRows = ()):
		leftIdx = np.where(self.weights[:, self.termsInfo[attribute]] <= threshold)[0]
		rightIdx = np.where(self.weights[:, self.termsInfo[attribute]] > threshold)[0]
		leftChild = np.array(list(set(leftIdx) - set(excludedRows)))
		rightChild = np.array(list(set(rightIdx) - set(excludedRows)))

		return leftChild, rightChild

	def attach_node(self, excludedRows = (), parentNode = None, direction = "left"):
		attrThresholds = self.pruning(excludedRows)
		if len(attrThresholds) > 0:
			attr, threshold = attrThresholds[0][0], attrThresholds[0][1]

			# create new node instance
			newNode = Node(attr, threshold, "root" if self.tree is None else "branch")
			if self.tree is None:
				self.tree = newNode

			# get left and right childs for the node
			left, right = self.get_child_nodes(attr, threshold, excludedRows)

			# get data exclusion for each child
			leftExclusion = left if excludedRows == () else np.append(left, excludedRows)
			rightExclusion = right if excludedRows == () else np.append(right, excludedRows)

			# get left and right data
			leftData = self.npdata[left]
			rightData = self.npdata[right]

			# count label occurence for each child
			leftLabel, leftCount = np.unique(leftData[:, -2], return_counts = True)
			rightLabel, rightCount = np.unique(rightData[:, -2], return_counts = True)

			leftDataCount = len(left)
			rightDataCount = len(right)

			labels = np.unique(np.append(leftLabel, rightLabel))
			labelCount = len(labels)

			# attach child node
			if parentNode is not None:
				if direction == "left":
					parentNode.set_left_child(newNode)
				
				elif direction == "right":
					parentNode.set_right_child(newNode)

			# set node type to label if there is only one label
			if labelCount == 1:
				newNode.set_type("leaf")
				newNode.set_label(labels[0])
			elif labelCount == 2:
				if len(leftLabel) == 1:
					leftLeafNode = Node(attr, threshold, "leaf")
					leftLeafNode.set_label(leftLabel[0])
					newNode.set_left_child(leftLeafNode)
				if len(rightLabel) == 1:
					rightLeafNode = Node(attr, threshold, "leaf")
					rightLeafNode.set_label(rightLabel[0])
					newNode.set_right_child(rightLeafNode)
			else:
				if rightDataCount > 0:
					self.attach_node(leftExclusion, newNode, "right")
				if leftDataCount > 0:
					self.attach_node(rightExclusion, newNode, "left")

	def train(self):
		self.calculate_total_entropy()
		self.attach_node()

	def traverse(self, row, vectors, currNode = None):
		# is there null coalesce?
		if currNode is None:
			currNode = self.tree

		if currNode is not None:
			if currNode.nodeType == "leaf":
				return currNode.label
			else:
				if vectors.weights[:, vectors.termIndex[currNode.attribute]][row] <= currNode.threshold:
					return self.traverse(row, vectors, currNode.left)
				else:
					return self.traverse(row, vectors, currNode.right)

		return False

	def fit(self, docs, labels):
		self.train()

	def predict(self, docs):
		vectors = TFIDF_optimized(docs)
		return np.array([self.traverse(i, vectors) for i, vec in enumerate(vectors.weights)])

	def score(self, data):
		predicted = self.predict(data["Review"])
		actual = np.array(data["Label"])
		at, cm = np.unique(predicted == actual, return_counts=True)
		return (0 if True not in at else (cm[0] if len(at) == 1 else cm[1])) / np.sum(cm)