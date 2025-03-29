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


import dataclasses
from pathlib import Path
from typing import Dict, List, Protocol, Tuple, Union, runtime_checkable

from gm3dh5._detail.types import FloatArrayLike, Int32ArrayLike, UInt8ArrayLike

from .geometry import Quaternion

__all__ = ["PhaseInfo", "Volume", "Label", "GM3DResultFileModel", "Exporter"]


@dataclasses.dataclass
class PhaseInfo:
    r"""Phase information of the data set.

    Parameters
    ----------
    id
        PhaseId used in the data set.
    name
        Name of the phase.
    unit_cell
        Unit cell parameters :math:`(a,b,c,\alpha,\beta,\gamma)` in Å and degrees.
    space_group
        Space group number according to the ITA.

    crystal_system
        Crystal system.

    universal_hermann_mauguin
        Hermann-Mauguin symbol.
    """

    id: int
    """PhaseId used in the data set."""

    name: str
    """Name of the phase."""

    unit_cell: Tuple[float, float, float, float, float, float]
    r"""Unit cell parameters :math:`(a,b,c,\alpha,\beta,\gamma)` in Å and degrees."""

    space_group: int
    """Space group number according to the ITA."""

    crystal_system: Union[str, None]
    """Crystal system."""

    universal_hermann_mauguin: Union[str, None]
    """Hermann-Mauguin symbol."""


@dataclasses.dataclass
class Label:
    """Label information of a mask.

    Parameters
    ----------
    id
        Id refers to the mask value of the data set.
    name
        Alias of the label.
    color
        Color of the label.
    """

    id: int
    """Id refers to the mask value of the data set."""

    name: str
    """Alias of the label."""

    color: bytes
    """Color of the label."""


@runtime_checkable
class Volume(Protocol):
    @property
    def spacing(self) -> Tuple[float, float, float]: ...
    @property
    def shape(self) -> Tuple[int, int, int]: ...
    @property
    def extent(self) -> Tuple[float, float, float]: ...
    @property
    def center(self) -> Tuple[float, float, float]: ...


@runtime_checkable
class GM3DResultFileModel(Volume, Protocol):
    @property
    def grainids(self) -> Int32ArrayLike: ...
    @property
    def mask(self) -> UInt8ArrayLike: ...  # labels or labelmask?
    @property
    def phaseid(self) -> UInt8ArrayLike: ...
    @property
    def completeness(self) -> FloatArrayLike: ...
    @property
    def rotations(self) -> Dict[int, Quaternion]: ...
    @property
    def phases(self) -> List[PhaseInfo]: ...


@runtime_checkable
class Exporter(Protocol):
    @property
    def suffix(self) -> str: ...

    @property
    def name(self) -> str: ...

    def dump(self, result_file: GM3DResultFileModel, filename: Union[str, Path]): ...
