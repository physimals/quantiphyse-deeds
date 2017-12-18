#!/usr/bin/env python
"""
Build Quantiphyse plugin for DEEDS
"""

import numpy
import os
import sys
import shutil

from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools.extension import Extension

desc = "Quantiphyse package for DEEDS"
version = "0.0.1"

# DEEDS extension
extensions = []
compile_args = []
link_args = []

if sys.platform.startswith('win'):
    compile_args.append('/EHsc')
    zlib = "zlib"
    extra_inc = "deeds/src/compat"
elif sys.platform.startswith('darwin'):
    link_args.append("-stdlib=libc++")
    extra_inc = "."

extensions.append(Extension("deeds.deeds_wrapper",
                 sources=['deeds/deeds_wrapper.pyx',
                          'deeds/src/TMI2013/deedsMSTssc.cpp'],
                 include_dirs=[numpy.get_include(), 
                               "deeds/src/TMI2013/", 
                               extra_inc],
                 language="c++", extra_compile_args=compile_args, extra_link_args=link_args))

# setup parameters
setup(name='fabber_qp',
      cmdclass={},
      version=version,
      description=desc,
      long_description=desc,
      author='Michael Chappell, Martin Craig',
      author_email='martin.craig@eng.ox.ac.uk',
      packages=['deeds'],
      include_package_data=True,
      data_files=[],
      setup_requires=[],
      install_requires=[],
      ext_modules=cythonize(extensions),
      classifiers=["Programming Language :: Python :: 2.7",
                   "Development Status:: 3 - Alpha",
                   'Programming Language :: Python',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   "Intended Audience :: Education",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: End Users/Desktop",
                   "Topic :: Scientific/Engineering :: Bio-Informatics",],
)

