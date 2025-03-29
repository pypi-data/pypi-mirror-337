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

import logging
from typing import Dict, List, Tuple, Union

import h5py
import numpy as np

from ._detail.types import FloatArrayLike, Int32ArrayLike, UInt8ArrayLike
from ._detail.utils import first_occurrence
from .geometry import Quaternion, Vec3
from .protocols import GM3DResultFileModel, Label, PhaseInfo

__all__ = ["GM3DResultFileReader"]


logger = logging.getLogger(__name__)


def _get_labels(file, groupname) -> Union[List[Label], None]:
    result = None
    label_groupname = groupname + "/Labels"
    if label_groupname in file:
        colors = labels = names = None
        labels_group = file[label_groupname]
        if "Colors" in labels_group:
            colors = labels_group["Colors"]
        if "Labels" in labels_group:
            labels = labels_group["Labels"][:]
        if "Names" in labels_group:
            names = labels_group["Names"][:]

        if labels is not None:
            result = []
            for l, n, c in zip(labels, names, colors):
                result.append(
                    Label(
                        id=int(l),
                        name=n.decode(),
                        color=c.tobytes(),
                    )
                )

    return result


class GM3DResultFileReader:
    """Read file contents of a GM3D Result File.

    Parameters
    ----------
    filepath
        Location of a file to read.

    Example
    -------
    >>> from gm3dh5.file import GM3DResultFileReader
    >>> with GM3DResultFileReader("example.h5") as f:
    >>>     f.completeness
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._file = None
        self.open()

    def __enter__(self) -> "GM3DResultFileReader":
        if not self._file:
            self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def __getitem__(self, subs):
        try:
            assert self._file, f"File '{self.filepath}' not open"
            assert subs in self._file, f"'{subs}' not found in file '{self.filepath}'"
            return self._file[subs]
        except Exception as ex:
            logger.error(ex)
            raise ex

    def _assert_is_result_file(self):
        file = self._file
        assert file, "File not open"
        assert "/LabDCT/Spacing" in file, "Spacing missing"
        assert "/LabDCT/Center" in file, "Center missing"
        assert "/LabDCT/Data" in file, "Data missing"
        assert self.rotation_convention != "Unknown", "Unknown rotation convention"
        for mandatory in ("GrainId", "Completeness", "PhaseId"):
            assert "/LabDCT/Data/" + mandatory in file, (
                f"Missing LabDCT data {mandatory}"
            )

    def open(self):
        try:
            assert h5py.is_hdf5(self.filepath), "Not a GM3D Result File"
            self._file = h5py.File(self.filepath, "r")
            self._assert_is_result_file()
        except Exception as ex:
            logger.error(f"Error opening file '{self.filepath}': {ex}")
            self.close()
            raise Exception(f"Error opening file {self.filepath}") from ex

    def close(self):
        if self._file:
            self._file.close()
            self._file = None

    def _get_data(self, name: str):
        return np.asarray(self["/LabDCT/Data/" + name][()])

    @property
    def version(self) -> int:
        try:
            return int(self["/Version"][0])
        except Exception:
            return -1

    @property
    def spacing(self) -> Tuple[float, float, float]:
        spacing = self["/LabDCT/Spacing"][:]
        return tuple(map(float, spacing))

    @property
    def shape(self) -> Tuple[int, int, int]:
        return tuple(map(int, self.grainids.shape))

    @property
    def extent(self) -> Tuple[float, float, float]:
        (zi, yi, xi) = self.shape
        (dx, dy, dz) = self.spacing
        return (dx * xi, dy * yi, dz * zi)

    @property
    def center(self) -> Tuple[float, float, float]:
        center = self["/LabDCT/Center"][:]
        return tuple(map(float, center))

    @property
    def grainids(self) -> Int32ArrayLike:
        return self._get_data("GrainId")

    @property
    def mask(self) -> UInt8ArrayLike:
        try:
            return self._get_data("Mask")
        except Exception:
            logger.warning("Using '/LabDCT/Data/PhaseId' instead")
            return self._get_data("PhaseId")

    @property
    def mask_labels(self) -> Union[List[Label], None]:
        try:
            return _get_labels(self._file, "/LabDCT")
        except Exception:
            logger.warning("Failed to extract label information from '/LabDCT'")
            return None

    @property
    def phaseid(self) -> UInt8ArrayLike:
        try:
            return self._get_data("PhaseId")
        except Exception:
            logger.warning("Using '/LabDCT/Data/Mask' instead")
            return self._get_data("Mask")

    @property
    def completeness(self) -> FloatArrayLike:
        return self._get_data("Completeness")

    @property
    def rotation_convention(self) -> str:
        _data_group = self["/LabDCT/Data"]
        for convention in ("Rodrigues", "Quaternion", "EulerZXZ", "EulerZYZ"):
            if convention in _data_group:
                return convention
        return "Unknown"

    @property
    def rotations(self) -> Dict[int, Quaternion]:
        convention = self.rotation_convention
        assert convention != "Unknown", "Unknown rotation convention"

        grainids, indices = first_occurrence(self.grainids)
        i, j, k = np.unravel_index(indices, self.shape)

        rotations = self._get_data(convention)
        selection = rotations[i, j, k].T  # -> convert to quaternion?
        if convention == "Quaternion":  # match convention
            q = Quaternion(*selection)
        elif convention == "Rodrigues":
            q = Quaternion.from_rodrigues(Vec3(*selection))
        elif convention == "EulerZXZ":
            q = Quaternion.from_euler_zxz(*selection)
        elif convention == "EulerZYZ":
            q = Quaternion.from_euler_zyz(*selection)

        return {int(id): rot for id, rot in zip(grainids, q) if id > 0}

    @property
    def phases(self) -> List[PhaseInfo]:
        def _system(ita):
            if ita < 0 or 230 < ita:
                raise ValueError("ITA number must be between 1 and 230")

            data = {
                2: "triclinic",
                15: "monoclinic",
                74: "orthorhombic",
                142: "tetragonal",
                167: "trigonal",
                194: "hexagonal",
                230: "cubic",
            }

            for d in data:
                if ita <= d:
                    return data[d]

        def _id(phase_id):
            try:
                return int(phase_id[-2:])
            except Exception as ex:
                raise IndexError(f"Unexpected format for PhaseId {phase_id}") from ex

        def _asstring(dataset):
            dset = None
            if dataset.shape == ():
                dset = dataset[()]
            elif dataset.shape == (1,):
                dset = dataset[0]
            return dset.decode()

        result = []
        for phase_id, phase_group in self["PhaseInfo"].items():
            phase_group["Name"][()]

            name = _asstring(phase_group["Name"])
            sg = int(phase_group["SpaceGroup"][0])
            hm = _asstring(phase_group["UniversalHermannMauguin"])
            uc = tuple(map(float, phase_group["UnitCell"][:]))
            result.append(
                PhaseInfo(
                    id=_id(phase_id),
                    name=name,
                    space_group=sg,
                    unit_cell=uc,
                    crystal_system=_system(sg),
                    universal_hermann_mauguin=hm,
                )
            )
        return result

    def export(self, filename: str, exporter=None, *args, **kwargs):
        r"""Export the result file.

        Parameters
        ----------
        filename:
            File name of the file to be exported. If the exporter is not specified, the
            exporter is determined by the file name suffix.

            Known suffixes are \*.tesr, \*.csv

        exporter:
            Specify the exporter explicitely, either by file name suffix, the :doc:`gm3dh5.protocols.Exporter` class
            or than :doc:`gm3dh5.protocols.Exporter` instance.

        **kwargs:
            Specify exporter options.

        See Also
        --------
        :doc:`gm3dh5.protocols.Exporter`,
        :doc:`gm3dh5.exporter.csv.CSVExporter`
        :doc:`gm3dh5.exporter.neper.NeperTesrExporter`
        """
        from .exporter import dump

        dump(self, filename=filename, exporter=exporter, *args, **kwargs)
