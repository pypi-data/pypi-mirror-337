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

from common import del_output, get_example_data, get_output, sha256file
import pytest

from gm3dh5.file import GM3DResultFileReader


def test_NeperTesrExporter():
    with GM3DResultFileReader(get_example_data("example.h5")) as f:
        f.export(get_output("example.tesr"))

        file_digest = "0bf2cf38c455ae5ea6d1c1b11bf360e764a755c2b23f2a167da599c6806f4807"
        assert file_digest == sha256file(get_output("example.tesr"))
        del_output("example.tesr")


def test_CSVExporter():
    with GM3DResultFileReader(get_example_data("example.h5")) as f:
        for convention in ("Rodrigues", "Quaternion", "EulerZXZ", "EulerZYZ"):
            f.export(get_output("example.csv"), rotation_convention=convention)

        # TODO: assertion missing
        # get_example_data("example.csv")

        del_output("example.csv")


def test_CSVExporterInstance():
    with GM3DResultFileReader(get_example_data("example.h5")) as f:
        from gm3dh5.exporter.csv import CSVExporter

        csv = CSVExporter(rotation_convention="EulerZXZ")
        f.export(get_output("example"), exporter=csv)

        del_output("example.csv")


def test_NotAnExporter():
    class test:
        pass

    with pytest.raises(Exception, match="invalid exporter") as e_info:
        with GM3DResultFileReader(get_example_data("example.h5")) as f:
            f.export(get_output("example"), exporter=test)


# test_CSVExporterInstance()
# test_NeperTesrExporter()
# test_CSVExporter()
