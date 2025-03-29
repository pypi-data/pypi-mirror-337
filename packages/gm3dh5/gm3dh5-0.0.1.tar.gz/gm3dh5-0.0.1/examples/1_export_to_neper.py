"""
===========================
Export to NEPER TESR Format
===========================

A short example how to export a GrainMapper3D Result File to Neper
`Raster Tessellation File <https://neper.info/doc/fileformat.html#raster-tessellation-file-tesr>`_.

For how to process the \\*.tesr file, please refer to the :ref:`neper-tutorial` tutorial or
to the `Neper documentation <https://neper.info/doc/tutorials/morpho_tesr_mesh.html>`_
"""

# %%
# Export to \*.tesr File Format
# ----------------------------
# The following minimal example create a tesr file

from gm3dh5.file import GM3DResultFileReader

with GM3DResultFileReader("example.h5") as f:
    f.export("example.tesr")


# %%
# Visualize with Neper
# --------------------
# The following command

# %%
# .. code-block:: bash
#
#    neper -V example.tesr -datavoxcol ori -datavoxcolscheme ipf -print example

########################################################################################
# generates the image:

# %%
# .. figure:: ../_static/example.png

# sphinx_gallery_thumbnail_path = "_static/example.png"
