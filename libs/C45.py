from math import log
import numpy as np

class C45():
        
    def __init__(self, db):
        self.db             = db
        self.total_entropy  = self.get_total_entropy()
        self.attributes     = self.db.select("attributes")
        self.split_query    = ""
        self.weight_query   = ""

        weights = self.db.query("SELECT attribute, weight FROM weights ORDER BY weight DESC")
        self.attr_weights   = np.asarray(weights)

        data = self.db.query("SELECT weights.*, preprocessed_data.label FROM weights LEFT JOIN preprocessed_data ON preprocessed_data.id = weights.id_document")
        self.data           = np.asarray(data)

        self.dfgx           = lambda attr, label, split, excluded_id: filter(lambda row: row[2] == attr and float(row[3]) > split and row[4] == label and row[1] not in excluded_id, self.data)
        self.dflx           = lambda attr, label, split, excluded_id: filter(lambda row: row[2] == attr and float(row[3]) <= split and row[4] == label and row[1] not in excluded_id, self.data)

    def get_data_split(self, attr, split_value, split_type = "greater", excluded_id = []):
        data_split = { "Positive": 0, "Negative": 0, "Neutral": 0 }

        if split_type == "greater":
            positive = self.dfgx(attr, "Berdampak positif", split_value, excluded_id)
            negative = self.dfgx(attr, "Berdampak negatif", split_value, excluded_id)
            neutral = self.dfgx(attr, "Netral", split_value, excluded_id)
        elif split_type == "less":
            positive = self.dflx(attr, "Berdampak positif", split_value, excluded_id)
            negative = self.dflx(attr, "Berdampak negatif", split_value, excluded_id)
            neutral = self.dflx(attr, "Netral", split_value, excluded_id)

        data_split["Positive"] = sum(1 for _ in positive)
        data_split["Negative"] = sum(1 for _ in negative)
        data_split["Neutral"] = sum(1 for _ in neutral)
        # for row in positive:
        #         data_split["Positive"] += 1

        # for row in negative:
        #         data_split["Negative"] += 1

        # for row in neutral:
        #         data_split["Neutral"] += 1

        return data_split

    def get_total_entropy(self):
        self.data = self.db.query("SELECT label, COUNT(id) AS total FROM preprocessed_data GROUP BY label")
        self.data = list(zip(*self.data))
        dlen = sum(self.data[1])
        total_entropy = 0
        for count in self.data[1]:
            total_entropy += (-1 * (count / dlen) * log(count / dlen, 10))
        return total_entropy

    def attribute_entropy(self):
        attrs = self.db.query("SELECT attribute, weight FROM weights ORDER BY weight DESC")
        attrs = np.asarray(attrs)
        # print(attrs[attrs[:,0] == "gojek"])
        # for i, row in enumerate(self.attributes):
        #     print(row[1])
        #     if i >= len(self.attributes) - 1:
        #         self.construct_weight_query(row[1], "ORDER BY weight DESC")
        #     else:
        #         self.construct_weight_query(row[1])
        # print(self.weight_query)
        # print(self.execute_weight_query())

    def gain(self, info):
    	return self.total_entropy - info

    def info(self, data, entropies):
        num_data = sum(sum(data, []))
        info = 0
        for d, entropy in zip(data, entropies):
            info += (sum(d) / num_data) * entropy
        return info

    def entropy(self, data):
        entropy = 0
        total = sum(data)
        for d in data:
            try:
                logged_val = log(d / total, 10)
            except:
                logged_val = 0
            entropy += (-1 * (d / total) * logged_val)
        return entropy

    # data = ((993, 2, 'praktis', 2.25780386641995, 'Berdampak positif', 8), (994, 2, 'praktis', 2.25780386641995, 'Berdampak negatif', 8))
    # fx = lambda label: filter(lambda row: row[4] == label, list(data))

    def construct_split_query(self, attr, split_value, split_type = "greater", excluded_id = []):
        if len(self.split_query) > 0:
            self.split_query += "UNION "

        idlen = len(excluded_id)

        sql = "SELECT weights.*, preprocessed_data.label, COUNT(preprocessed_data.label) AS total FROM weights LEFT JOIN preprocessed_data ON preprocessed_data.id = weights.id_document WHERE attribute = '" + attr + "'"
        
        if split_type == "greater":
            sql += " AND weight > " + str(split_value)
        else:
            sql += " AND weight <= " + str(split_value)

        if idlen > 0:
            excluded_id = "(" + ",".join(excluded_id) + ")"
            sql += " AND id_document NOT IN " + excluded_id
        
        sql += " GROUP BY preprocessed_data.label "
        self.split_value += sql

    def reset_split_query(self):
        self.split_query = ""

    def execute_split_query(self):
        return self.db.query(self.split_query)

    # def get_data_split(self, attr, split_value, split_type = "greater", excluded_id = []):
    #     idlen = len(excluded_id)
        
    #     sql = "SELECT weights.*, preprocessed_data.label, COUNT(preprocessed_data.label) AS total FROM weights LEFT JOIN preprocessed_data ON preprocessed_data.id = weights.id_document WHERE attribute = '" + attr + "'"
        
    #     if split_type == "greater":
    #         sql += " AND weight > " + str(split_value)
    #     else:
    #         sql += " AND weight <= " + str(split_value)

    #     if idlen > 0:
    #         excluded_id = "(" + ",".join(excluded_id) + ")"
    #         sql += " AND id_document NOT IN " + excluded_id
        
    #     sql += " GROUP BY preprocessed_data.label"
        
    #     return self.db.query(sql)

    def construct_weight_query(self, attr, order = ""):
        if len(self.weight_query) > 0:
            self.weight_query += "UNION "

        sql = "SELECT attribute, weight FROM weights WHERE attribute='" + attr + "' "
        if len(order) > 0:
            sql += order

        self.weight_query += sql

    def execute_weight_query(self):
        return self.db.query(self.weight_query)

    def reset_weight_query(self):
        self.weight_query = ""

    def discretize_attribute(self, attr, excluded_id = []):
        weights = self.attr_weights[[self.attr_weights[:, 0] == attr]]

        possible_splits = []
        for idx in range(len(weights) - 1):
            possible_splits.append((float(weights[idx][1]) + float(weights[idx + 1][1])) / 2)

        possible_splits = list(set(possible_splits)) # remove duplicates
        gains = {}
        
        for split in possible_splits:
            greater = self.get_data_split(attr, float(split), "greater", excluded_id)
            less = self.get_data_split(attr, float(split), "less", excluded_id)
            print(greater)
            print(less)
        #     greater_list = list(zip(*greater))
        #     less_list = list(zip(*less))
        #     greater_ent = self.entropy(greater_list[5])
        #     less_ent = self.entropy(less_list[5])
        #     ent = [greater_ent, less_ent]
        #     data = [list(greater_list[5]), list(less_list[5])]
        #     gains[split] = self.gain(self.info(data, ent))
        # gains = sorted(gains.items(), key = lambda x: x[1], reverse = True)
        # return gains[0]