import cython
cimport cython

import numpy as np
cimport numpy as np

def main():
    cdef np.ndarray[np.int32_t, ndim=2] data
    data = np.array([[1, 2], [3, 4]])
    print(data)