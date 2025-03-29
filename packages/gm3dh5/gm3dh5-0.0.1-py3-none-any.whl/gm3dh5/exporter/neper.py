#!/usr/bin/env python
#
# Copyright 2025 Xnovo Technology ApS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an  "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import io
import logging
from pathlib import Path
from typing import Iterable, Union

import numpy as np

from gm3dh5.protocols import Exporter, GM3DResultFileModel

__all__ = ["NeperTesrExporter"]


class NeperTesrExporter(Exporter):
    r"""Export GrainMapper3D Result File to Neper Raster Tessellation File (\*.tesr)."""

    @property
    def name(self):
        return "Neper Tesselation"

    @property
    def suffix(self):
        return ".tesr"

    def dump(self, result_file: GM3DResultFileModel, filename: Union[str, Path]):
        with open(filename, "wb") as fp:
            _neper_tesr(fp, result_file)
            _neper_cell(fp, result_file)
            _neper_data(fp, result_file)
            _neper_end(fp)


def _write_line(fp: io.BufferedWriter, line: str):
    fp.write(line.encode())
    fp.write(b"\n")


def _write_lines(fp: io.BufferedWriter, lines: Iterable[str]):
    for line in lines:
        _write_line(fp, line)


def _neper_tesr(fp: io.BufferedWriter, result_file: GM3DResultFileModel):
    (zi, yi, xi) = result_file.shape
    (dx, dy, dz) = result_file.spacing
    _write_lines(
        fp,
        (
            "***tesr",
            " **format",
            "   2.2",
            " **general",
            "   3",
            f"   {xi} {yi} {zi}",  # dimensions
            f"   {dx:0.12f} {dy:0.12f} {dz:0.12f}",  # spacings
        ),
    )


def _neper_cell(fp: io.BufferedWriter, result_file: GM3DResultFileModel):
    def _wrap(lst, size):
        line = "  "
        result = []
        for s in map(str, lst):
            if len(line) + len(s) < size:
                line += " "
            else:
                result.append(line)
                line = ""  # flush
            line += s
        result.append(line)
        return result

    if len(result_file.phases) != 1:
        logging.warning("Only single phase supported. exporting only the first phase")

    phase = result_file.phases[0]
    crysym = phase.crystal_system
    if crysym not in ("triclinic", "hexagonal", "cubic"):
        raise ValueError(f"Neper does not support {crysym} crystal system")

    # result_file.get_orientations()
    rotations = result_file.rotations
    grainids = rotations.keys()

    _write_lines(
        fp,
        (
            " **cell",
            f"   {len(grainids)}",
            "  *id",
            *_wrap(grainids, 75),
            "  *ori",
            "   rodrigues:passive",
        ),
    )

    for q in rotations.values():
        r = q.as_rodrigues()
        _write_line(fp, f"{r.x:17.12f} {r.y:17.12f} {r.z:17.12f}")

    _write_lines(
        fp,
        (
            "  *crysym",
            f"   {crysym}",
        ),
    )


def _neper_data(fp: io.BufferedWriter, result_file: GM3DResultFileModel):
    grainid = result_file.grainids
    max_grainid = grainid.max()

    for bits, dtype in ((8, np.uint8), (16, np.uint16), (32, np.uint32)):
        if max_grainid < 2**bits:
            format = f"binary{bits}"
            grainid = grainid.astype(dtype)
            break

    _write_lines(
        fp,
        (
            " **data",
            f"   {format}",
        ),
    )

    fp.write(grainid.data)
    fp.write(b"\n")


def _neper_end(fp: io.BufferedWriter):
    fp.write(b"***end")
