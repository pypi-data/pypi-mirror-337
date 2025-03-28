# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "readme.rst"), encoding="utf8") as f:
    long_description = f.read()

setup(
    name="spatial_inventory_rollback",
    version="1.1.0",
    description="GCBM Spatial Inventory Rollback Tool ",
    long_description=long_description,
    url="https://github.com/Simpleshell3/spatial_inventory_rollback",
    author="Moja.global",
    author_email="",
    license="MPL2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
    ],
    keywords="moja.global",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
        'GDAL==3.4.3',
        'jupytext==1.16.7',
        'libcbm==2.6.6',
        'mojadata==4.1.5',
        'nbconvert==7.16.6',
        'nbformat==5.10.4',
        'numba==0.61.0',
        'numpy==2.2.4',
        'pandas==2.2.3',
        'papermill==2.6.0',
        'psutil==7.0.0',
        'scipy==1.15.2',
        'setuptools==75.8.0',
    ],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
    python_requires=">=3.7"
)
