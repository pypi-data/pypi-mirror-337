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
from typing import Type, Union

from gm3dh5.exporter.csv import CSVExporter
from gm3dh5.exporter.neper import NeperTesrExporter
from gm3dh5.protocols import Exporter, GM3DResultFileModel

__all__ = ["dump"]


_KNOWN_EXPORTER = (NeperTesrExporter, CSVExporter)
_KNOWN_EXTENSIONS = {x().suffix: x for x in _KNOWN_EXPORTER}


def _find_by_suffix(suffix: str) -> Type[Exporter]:
    if suffix in _KNOWN_EXTENSIONS:
        return _KNOWN_EXTENSIONS[suffix]
    raise ValueError(
        f"Failed to determine export format based on suffix: '{suffix}'."
        "Please specify either a known export extension or the exporter explicitly."
    )


def _find_exporter(exporter: str) -> Type[Exporter]:
    try:
        return _find_by_suffix(f".{exporter.lower()}")
    except Exception as ex:
        raise ValueError(
            f"Unknown export format: '{exporter}'."
            "Please specify either a known export extension or the exporter explicitly."
        ) from ex


def dump(
    data: GM3DResultFileModel,
    filename: Union[str, Path],
    exporter: Union[Type[Exporter], Exporter, str, None] = None,
    *args,
    **kwargs,
):
    r"""Dump a result file into a specific exporter format.

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
    assert isinstance(data, GM3DResultFileModel), "Can only dump GM3DResultFileModel"

    filepath = Path(filename)
    if exporter is None:
        exporter = _find_by_suffix(filepath.suffix)
    elif isinstance(exporter, str):
        exporter = _find_exporter(exporter)

    if not isinstance(exporter, Exporter):
        raise ValueError(f"invalid exporter {exporter}")

    # construct exporter if necessary
    ex = exporter(*args, **kwargs) if isinstance(exporter, type) else exporter

    try:
        filelocation = filepath.with_suffix(ex.suffix)
        ex.dump(data, filelocation)
    except Exception as exeption:
        raise Exception(f"Failed to export to format '{ex.name}'") from exeption
