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

import hashlib
import os
import pathlib
from typing import Iterable

ROOT = pathlib.Path(__file__).parent.parent

DOCPATH = os.path.normpath(os.path.join(ROOT, "doc"))
EXAMPLEPATH = os.path.normpath(os.path.join(ROOT, "examples"))
TESTPATH = os.path.normpath(os.path.join(ROOT, "tests"))


def get_example_data(data: str):
    return os.path.join(EXAMPLEPATH, data)


def get_output(data: str):
    return os.path.join(TESTPATH, data)


def del_output(data: str):
    try:
        path = get_output(data)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def sha256file(filename):
    # note: only with py11 : hashlib.file_digest(f, "sha256").hexdigest()
    _bufsize = 2**18
    digestobj = hashlib.sha256()
    with open(filename, "rb", buffering=0) as f:
        buf = bytearray(_bufsize)  # Reusable buffer to reduce allocations.
        view = memoryview(buf)
        while True:
            size = f.readinto(buf)
            if size == 0:
                break  # EOF
            digestobj.update(view[:size])
    return digestobj.hexdigest()


def sha256string(d):
    # note: only with py11 : hashlib.file_digest(f, "sha256").hexdigest()
    digestobj = hashlib.sha256()
    digestobj.update(repr(d).encode())
    return digestobj.hexdigest()


def sha256array(items: Iterable):
    digestobj = hashlib.sha256()

    for item in items:
        digestobj.update(item)

    return digestobj.hexdigest()
