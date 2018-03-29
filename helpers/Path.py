import os.path

def relative_path(filepath):
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, filepath)
    return path