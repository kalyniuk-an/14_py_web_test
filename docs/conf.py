import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Contacts API"
author = "Anastasiia"
release = "1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "uk"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]