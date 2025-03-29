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
from typing import Union

from gm3dh5.protocols import Exporter, GM3DResultFileModel

class CSVExporter(Exporter):
    def __init__(
        self,
        rotation_convention: str | None = None,
        delimiter: str | None = None,
        degrees: bool = True,
    ) -> None: ...
    @property
    def name(self): ...
    @property
    def suffix(self): ...
    def dump(self, result_file: GM3DResultFileModel, filename: Union[str, Path]): ...
