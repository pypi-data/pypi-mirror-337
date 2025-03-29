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

from importlib.util import find_spec

import numpy as np

__all__ = ["first_occurrence", "set_module"]


def first_occurrence(ids):
    if ids.size == 0:
        return np.array([], dtype=ids.dtype), np.array([], dtype=int)

    # if max(ids) is large, bincount is a very long array
    ids = ids.ravel()
    counts = np.bincount(ids)
    index1 = np.zeros(counts.size, dtype=int)
    index1[ids[::-1]] = np.arange(ids.size - 1, -1, -1, dtype=int)
    index1 = index1[counts > 0]
    return ids[index1], index1


try:
    # if numba is installed
    if find_spec("numba") is not None:
        import numba

        @numba.njit(cache=True)
        def first_occurrence_(ids: np.ndarray):
            ids = ids.ravel()
            m = ids.max() + 1
            result = np.full(m, -1, dtype=np.int64)
            for x in range(ids.size):
                if result[ids[x]] == -1:
                    result[ids[x]] = x
            result = result[result > -1]
            return ids[result], result

        first_occurrence = first_occurrence_
except Exception:
    pass  # when loading directly from wheel numba may not work


def set_module(name, func):
    func.__module__ = name
