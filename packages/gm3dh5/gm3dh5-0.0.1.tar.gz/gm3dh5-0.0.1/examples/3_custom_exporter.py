"""
===============
Custom Exporter
===============

This example demonstrates how to implement a simple exporter
"""


# %%
# Define a Custom Exporter
# ------------------------
# Dump the grain id into a binary file

from pathlib import Path
from typing import Union

from gm3dh5.file import GM3DResultFileReader
from gm3dh5.protocols import Exporter, GM3DResultFileModel


class GrainIdExporter(Exporter):
    @property
    def suffix(self) -> str:
        return ".grainids"

    @property
    def name(self) -> str:
        return "Custom GrainId Exporter"

    def dump(self, result_file: GM3DResultFileModel, filename: Union[str, Path]):
        with open(filename, "wb") as fp:
            fp.write(result_file.grainids.data)


# %%
# Run the Exporter
# ----------------
# The GrainIdExporter will create a file named "example.grainids"

with GM3DResultFileReader("example.h5") as f:
    f.export("example", exporter=GrainIdExporter)


# %%
# Import the Exported Data
# ------------------------

with open("example.grainids", "rb") as fp:
    ids = fp.read()

########################################################################################
# convert back to numpy array

import numpy as np

np.frombuffer(ids, dtype=np.int32)

########################################################################################
# or read it directly from with numpy from the file
np.fromfile("example.grainids", dtype=np.int32)

# %%
#

# sphinx_gallery_thumbnail_path = "_static/Al-c.png"
