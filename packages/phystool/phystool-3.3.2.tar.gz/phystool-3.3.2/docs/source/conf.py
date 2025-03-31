project = 'phystool'
author = 'Jérome Dufour'

release = '0.1'
version = '0.1.0'

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
]

html_theme = "sphinx_rtd_theme"

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))
