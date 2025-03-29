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

from typing import Generic, TypeVar, Union

from numpy import bool_ as bool_, float32, generic, int32, uint8

try:
    from numpy._typing import NDArray
except ModuleNotFoundError:
    # old numpy may not support typing module
    from numpy import ndarray

    _ScalarType_co = TypeVar("_ScalarType_co", bound=generic, covariant=True)

    class NDArray(ndarray, Generic[_ScalarType_co]):
        pass

except Exception:
    pass

ArrayLike = Union[NDArray, float]
ArrayNoneLike = Union[ArrayLike, None]

BoolArrayLike = Union[NDArray[bool_], bool]
UInt8ArrayLike = Union[NDArray[uint8], uint8]
FloatArrayLike = Union[NDArray[float32], float32]
Int32ArrayLike = Union[NDArray[int32], int32]
