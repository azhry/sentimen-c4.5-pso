from math import log

class C45():
        
    def __init__(self, data, label_count):
        self.data			= data
        self.label_count 	= label_count

    def total_entropy(self):
    	dlen = len(self.data)
    	total_entropy = 0
    	for label, count in self.label_count.items():
    		total_entropy += (-1 * (count / dlen) * log(count / dlen, 10))
    	return total_entropy

    def attribute_entropy(self):
    	pass

    def gain(self):
    	pass

    def discretize_attribute(self):
    	pass