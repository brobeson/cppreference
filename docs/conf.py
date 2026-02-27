"""Configuration file for the Sphinx documentation builder."""

import os.path
import sys

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# pylint: disable=invalid-name
# cspell: words extlinks furo
# mypy: ignore-errors

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "CppReference"
project_copyright = "2026, brobeson"
author = "brobeson"
version = "0.0.0"
release = "0.0.0"
highlight_language = "cpp"

sys.path.insert(0, os.path.abspath("../"))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = [
#     "sphinx.ext.autodoc",
#     "sphinx.ext.extlinks",
#     "sphinx.ext.napoleon",
#     "sphinx_copybutton",
#     "sphinx_inline_tabs",
# ]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = project
html_theme_options = {
    "dark_css_variables": {"color-announcement-background": "#ff5252"},
    "announcement": "This is alpha documentation.",
}

copybutton_exclude = ".linenos, .gp, .go"
# extlinks = {"issue": ("https://github.com/brobeson/Rayne/issues/%s", "issue %s")}
