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

from pathlib import Path
from typing import List, Tuple, Union

import numpy as np

from ..geometry import Quaternion
from ..protocols import Exporter, GM3DResultFileModel, PhaseInfo

__all__ = ["CSVExporter"]  # help Sphinx!


class CSVExporter(Exporter):
    r"""Export GrainMapper3D Result File to comma seperated value (\*.csv) file.

    Parameters
    ----------
    rotation_convention
        Parameterization of the rotation, either:

        * "Rodrigues" (default if None)
        * "Quaternion"
        * "EulerZXZ"
        * "EulerZYZ"

    delimiter
        Either ";" (default) or ",".
    degrees
        Export Euler angles in degrees if True (default) or radians if False.
    """

    def __init__(
        self,
        rotation_convention: Union[str, None] = None,
        delimiter: Union[str, None] = None,
        degrees: bool = True,
    ) -> None:
        if rotation_convention is None:
            rotation_convention = "Rodrigues"
        assert rotation_convention in (
            "Rodrigues",
            "Quaternion",
            "EulerZXZ",
            "EulerZYZ",
        ), f"Invalid rotation convention '{rotation_convention}'"
        self.rotation_convention = rotation_convention

        if delimiter is None:
            delimiter = ";"
        assert delimiter in (";", ","), f"Invalid delimiter '{delimiter}'"
        self.delimiter = delimiter
        self.degrees = degrees

    @property
    def name(self):
        return "GrainMapper3D Centroid File"

    @property
    def suffix(self):
        return ".csv"

    def dump(self, result_file: GM3DResultFileModel, filename: Union[str, Path]):
        with open(filename, "w") as fp:
            centroids = _weighted_centroids(result_file)
            rotations = result_file.rotations

            fp.write(_format_header(self, result_file.phases))
            for k in sorted(rotations.keys()):
                if k in centroids:
                    line = self.delimiter.join(
                        (
                            f"{k:7d}",
                            *_format_centroid(centroids[k]),
                            *_format_rotation(self, rotations[k]),
                        )
                    )
                    fp.write(line + "\n")


def _weighted_centroids(result_file: GM3DResultFileModel):
    c = np.array(result_file.center)
    e = np.array(result_file.extent)
    s = np.array(result_file.spacing)

    # note that storage shape differs
    (zi, yi, xi) = result_file.shape

    s1 = c - e / 2 + s / 2  # center of voxel
    s2 = c + e / 2 - s / 2
    s = 1000.0  # um
    cx = s * np.linspace(s1[0], s2[0], xi)
    cy = s * np.linspace(s1[1], s2[1], yi)
    cz = s * np.linspace(s1[2], s2[2], zi)

    g = result_file.grainids.ravel()
    c = result_file.completeness.ravel()
    c[np.logical_not(np.isfinite(c))] = 0

    normalizer = np.bincount(g, weights=c)
    w = cx[np.newaxis, np.newaxis, :] * result_file.completeness
    cx = np.bincount(g, weights=w.ravel()) / normalizer
    w = cy[np.newaxis, :, np.newaxis] * result_file.completeness
    cy = np.bincount(g, weights=w.ravel()) / normalizer
    w = cz[:, np.newaxis, np.newaxis] * result_file.completeness
    cz = np.bincount(g, weights=w.ravel()) / normalizer

    gs = np.bincount(g)  # grainsize
    voxel_vol = s**3 * np.prod(result_file.spacing)
    esd = np.power(6 / np.pi * gs * voxel_vol, 1 / 3)
    comp = 100 * np.bincount(g, weights=c) / gs  # percent
    return {
        i: (cxx, cyy, czz, cm, e)
        for i, (cxx, cyy, czz, cm, e) in enumerate(zip(cx, cy, cz, comp, esd))
        if i > 0
    }


def _format_float(x) -> str:
    return f"{x:15.6f}"


def _format_centroid(c) -> Tuple[str, ...]:
    return tuple(map(_format_float, c))


def _format_rotation(exporter: CSVExporter, c: Quaternion) -> Tuple[str, ...]:
    if exporter.rotation_convention == "Rodrigues":
        data = c.as_rodrigues().asarray()
    elif exporter.rotation_convention == "EulerZXZ":
        data = np.asarray(c.as_euler_zxz())
    elif exporter.rotation_convention == "EulerZYZ":
        data = np.asarray(c.as_euler_zyz())
    else:
        data = np.asarray(c.aslist())

    if exporter.degrees and exporter.rotation_convention in ("EulerZXZ", "EulerZYZ"):
        data = np.degrees(data)

    return tuple(map(_format_float, data))


def _format_header(exporter: CSVExporter, phase_list: List[PhaseInfo]) -> str:
    # Phase 1 "Aluminum" "m-3m" 4.0496 4.0496 4.0496 90.0000 90.0000 90.0000
    # GrainId;PhaseId;X[um];Y[um];Z[um];RodX;RodY;RodZ;Completeness[%];ESD[um]

    header = ""
    for phase in phase_list:
        uc = " ".join(tuple(map(lambda x: f"{x:.4f}", phase.unit_cell)))
        header += f'#Phase {phase.id} "{phase.name}" "{phase.universal_hermann_mauguin}" {uc}\n'

    centroid = ("X[um]", "Y[um]", "Z[um]", "Completeness[%]", "ESD[um]")
    if exporter.rotation_convention == "Rodrigues":
        rot = ("RodX", "RodY", "RodZ")
    elif exporter.rotation_convention == "EulerZXZ":
        rot = ("phi1", "Phi", "phi2")
    elif exporter.rotation_convention == "EulerZYZ":
        rot = ("alpha", "beta", "gamma")
    else:
        rot = ("QuatA", "QuatB", "QuatC", "QuatD")

    fields = ["GrainId", *centroid, *rot]
    for i in range(1, len(fields)):
        fields[i] = f"{fields[i]:>15}"

    header += exporter.delimiter.join(fields) + "\n"
    return header
