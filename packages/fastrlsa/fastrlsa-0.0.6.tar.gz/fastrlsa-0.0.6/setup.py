import numpy as np
from distutils.core import setup, Extension

rlsa_module = Extension("fastrlsa", sources=["fastrlsa/fastrlsa.c"], include_dirs=[np.get_include()])


setup(
    name="fastrlsa",
    version="0.0.6",
    description="Run Length Smoothing Algorithm",
    install_requires=["numpy"],
    ext_modules=[rlsa_module],
    packages=["fastrlsa"],
)
