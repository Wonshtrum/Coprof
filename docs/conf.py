# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import shutil
import sphinx_rtd_theme
import recommonmark

sys.path.insert(0, os.path.abspath('../src/coprof'))


# -- Project information -----------------------------------------------------

project = 'Coprof'
copyright = '2021, Eloi Démolis'
author = 'Eloi Démolis'

def _copy_readme():
    print('copying readme')
    shutil.copy('../README.md', './readme_copy.md')

def _get_version():
    with open('../VERSION', 'r') as fin:
        ver = fin.read()
    ver_split = [key for key in ver.split('.') if key]
    if len(ver_split) >= 3:
        release = ".".join(ver.split('.')[:3])
        version = ".".join(ver.split('.')[:2])
    elif len(ver_split) == 2:
        release = "%s.0" % ver
        version = ver
    elif len(ver_split) == 1:
        release = "%s.0.0" % ver.replace('.', '')
        version = "%s.0" % ver.replace('.', '')
    return release, version

release, version = _get_version()
_copy_readme()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'recommonmark',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']