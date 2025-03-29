# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from gm3dh5.__about__ import __version__ as ver

project = "gm3dh5"
copyright = "2025, Xnovo Technology ApS"
author = "Xnovo Technology ApS"
version = ver

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx_codeautolink",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "numpydoc",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

pygments_style = "sphinx"
highlight_language = "python3"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "logo": {
        "image_light": "_static/logo-light.svg",
        "image_dark": "_static/logo-dark.svg",
    },
    "collapse_navigation": True,
    "external_links": [
        {
            "name": "GrainMapper3D",
            "url": "https://xnovotech.com/3d-crystallographic-imaging-software/",
        },
    ],
    "icon_links": [
        {
            "name": "PyPi",
            "url": "https://pypi.org/project/gm3dh5/",
            "icon": "fa-brands fa-python",
        },
        {
            "name": "Github",
            "url": "https://github.com/xnovotech/gm3dh5/",
            "icon": "fa-brands fa-github",
        },
    ],
    "header_links_before_dropdown": 6,
    "navigation_with_keys": True,
    "show_toc_level": 2,
    "navbar_end": [
        "search-button",
        "theme-switcher",
        "navbar-icon-links",
    ],
    "navbar_persistent": [],
    # "secondary_sidebar_items":
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "sg_download_links", "sg_launcher_links"],
        "index": [],
    },
    # "search_as_you_type": True, -- appears not not to work
    # "show_version_warning_banner": True,
}
html_context = {
    "doc_path": "doc",
    # "manifest_parameters": mf_params,
    # "contributions": contribs,
}
html_static_path = ["_static"]
##sphinx_gallery_thumbnail_path = "_static/Al-c.png"
html_copy_source = False
html_show_sourcelink = False
html_use_modindex = True
html_file_suffix = ".html"
html_show_sphinx = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {"reference": [], "index": []}


# sphinx_copybutton
# -----------------
# Exclude traditional Python prompts from the copied code
copybutton_prompt_text = r">>> ?|\.\.\. "
copybutton_prompt_is_regexp = True


# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
# sphinx.ext.autodoc
# ------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autosummary_ignore_module_all = False
autosummary_imported_members = True
autodoc_typehints_format = "short"
autodoc_default_options = {
    "show-inheritance": True,
}

# sphinx.ext.autosectionlabel
# ---------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
autosectionlabel_prefix_document = True  # Unique targets


# numpydoc
# --------
# https://numpydoc.readthedocs.io
numpydoc_show_class_members = False
numpydoc_use_plots = True
numpydoc_xref_param_type = True
# fmt: off
numpydoc_validation_checks = {
    "all",   # All but the following:
    "ES01",
    "EX01",
    "GL01",
    "GL02",
    "GL07",
    "GL08",
    "PR01",
    "PR02",
    "PR04",
    "RT01",
    "SA01",
    "SA04",
    "SS06",
    "YD01",
}
# fmt: on

# matplotlib.sphinxext.plot_directive
# -----------------------------------
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html
plot_formats = ["png"]
plot_html_show_source_link = False
plot_html_show_formats = False
plot_include_source = True


# Sphinx-Gallery
# --------------
# https://sphinx-gallery.github.io
sphinx_gallery_conf = {
    "backreferences_dir": "reference/generated",
    "doc_module": ("gm3dh5",),
    "examples_dirs": "../../examples",
    "filename_pattern": "^((?!sgskip).)*$",
    "gallery_dirs": "examples",
    "reference_url": {"gm3dh5": None},
    "run_stale_examples": False,
    "show_memory": False,  # True is really slow (and previously crashed) on macOS...
    "download_all_examples": False,
    "within_subsection_order": "FileNameSortKey",
}
autosummary_generate = True


# -----------------------------------------------------------------------------
# Intersphinx configuration
# -----------------------------------------------------------------------------
# intersphinx_mapping = {
#     "neps": ("https://numpy.org/neps", None),
#     "python": ("https://docs.python.org/3", None),
#     "scipy": ("https://docs.scipy.org/doc/scipy", None),
#     "matplotlib": ("https://matplotlib.org/stable", None),
#     "imageio": ("https://imageio.readthedocs.io/en/stable", None),
#     "skimage": ("https://scikit-image.org/docs/stable", None),
#     "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
#     "scipy-lecture-notes": ("https://scipy-lectures.org", None),
#     "pytest": ("https://docs.pytest.org/en/stable", None),
#     "numpy-tutorials": ("https://numpy.org/numpy-tutorials", None),
#     "numpydoc": ("https://numpydoc.readthedocs.io/en/latest", None),
#     "dlpack": ("https://dmlc.github.io/dlpack/latest", None),
# }

intersphinx_mapping = {
    "h5py": ("https://docs.h5py.org/en/stable", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "numba": ("https://numba.readthedocs.io/en/latest", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "numpydoc": ("https://numpydoc.readthedocs.io/en/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "pytest": ("https://docs.pytest.org/en/stable", None),
    "python": ("https://docs.python.org/3", None),
    "skimage": ("https://scikit-image.org/docs/stable", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}


def setup(app):
    """Sphinx setup function."""
    app.add_css_file("theme_override.css")
    app.add_css_file("hide_links.css")
