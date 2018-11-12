import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "revisions" else "revisions/..")

from entities.Storage import Storage

s = Storage()

for i in range(10):
	tree = s.load(f"../data/models/tree{i + 1}.pckl")
	tree.show_tree()
	break