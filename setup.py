#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
	Coprof
"""

from glob import glob
from os import path
from setuptools import find_packages, setup

NAME = "Coprof"
VERSION = "0.1.0"

# To install the library, run the following
#
# pytjon setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
	long_description = f.read()

setup(
	name=NAME,
	version=VERSION,
	description="Compare Profiling",
	long_description=long_description,
	long_description_content_type="text/markdown",
	keywords=["gprof"],
	install_requires=[
		"setuptools",
		"matplotlib",
		"click",
	],
	author="Eloi Démolis",
	author_email="coop@cerfacs.fr",
	url="http://cerfacs.fr/coop",
	packages=find_packages("src"),
	package_dir={"": "src"},
	py_modules=[path.splitext(path.basename(path))[0] for path in glob("src/*.py")],
	include_package_data=True,
	zip_safe=False,
	entry_points={
		"console_scripts": [
			"coprof = coprof.cli:main_cli",
		],
	},
)
