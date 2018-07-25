# from sklearn import tree
# from libs.TFIDF_revised import TFIDF_revised
# from entities.Storage import Storage
# from libs.C45 import C45
# from sklearn.externals.six import StringIO  
# from IPython.display import Image
# import pydotplus

# clf = tree.DecisionTreeClassifier()
# s = Storage()

# for i in range(1):
# 	train, test = (s.load(f"data/folds/train{i + 1}.pckl"), s.load(f"data/folds/test{i + 1}.pckl"))
# 	tfidf = TFIDF_revised(train["Review"])
# 	clf = clf.fit(tfidf.weights, train["Label"])
# 	file = open(f"tree{i}.txt", "w")
# 	tree.export_graphviz(clf, out_file=file, feature_names=tfidf.count_vect.get_feature_names(), class_names=list(train["Label"]), filled=True)

# from entities.Storage import Storage
# from libs.TFIDF_revised import TFIDF_revised
# from sklearn.feature_selection import mutual_info_classif
# from sklearn.feature_extraction.text import CountVectorizer

# s = Storage()
# train, test = (s.load(f"data/folds/train{1}.pckl"), s.load(f"data/folds/test{1}.pckl"))

# tfidf = TFIDF_revised(train["Review"])

# res = dict(zip(tfidf.count_vect.get_feature_names(), mutual_info_classif(tfidf.weights[0:4], train.iloc[0:4]["Label"], discrete_features=False, random_state=100)))

# print(sorted(res.items(), key=lambda x: x[1], reverse=True))

