from setuptools import setup, find_packages
from Cython.Build import cythonize
import os


def list_py_files(root_dir):
    py_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith(
                "__main__"
            ):
                py_files.append(os.path.join(dirpath, filename))
    return py_files


setup(
    name="quadible-data-pipeline",
    packages=find_packages(),
    ext_modules=cythonize(
        list_py_files("qink/lib"), compiler_directives={"language_level": "3"}
    ),
    zip_safe=False,
)
