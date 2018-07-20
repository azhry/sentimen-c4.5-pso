from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
	name = "Cython package for PSO - C4.5",
	ext_modules = cythonize(["*.pyx"]),
	include_dirs = [numpy.get_include()]
)