from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils.extension import Extension
from setuptools import setup

import numpy

setup(
    packages=["choldate", "choldate.test"],
    package_dir={
        "choldate": "choldate",
        "choldate.test": "choldate/test",
    },
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(
        [
            Extension(
                "choldate._choldate",
                ["choldate/_choldate.pyx"],
                include_dirs=[numpy.get_include()],
            )
        ]
    ),
    requires=["numpy", "cython"],
)
