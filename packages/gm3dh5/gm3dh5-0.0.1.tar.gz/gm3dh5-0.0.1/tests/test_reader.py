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

from common import sha256array, sha256string
from test_exporter import get_example_data

from gm3dh5.file import GM3DResultFileReader


def test_GM3DResultFileReader():
    with GM3DResultFileReader(get_example_data("example.h5")) as f:
        assert f.version == 5
        assert f.center == (0, 0, 0)
        assert f.extent == (0.5, 0.5, 1)
        assert f.rotation_convention == "Rodrigues"
        phases_digist = (
            "004dcafaa88ecdcc9bf7726b9b9845be856bf1d011e73e35f9384dea6b5bd0d4"
        )
        assert phases_digist == sha256string(f.phases)

        assert (
            sha256array((f.completeness, f.grainids, f.mask, f.grainids))
            == "b7719e9c87c6ce9f22d4a522bd48ffa61f21ea367f43cefc0d808032ac3b8343"
        )


# test_GM3DResultFileReader()
