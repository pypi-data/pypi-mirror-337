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

from typing import Tuple


def get_rgba(color: bytes) -> Tuple[int, ...]:
    """Convert color bytes array into a (r,g,b,a) int-tuple with values [0,255]

    Parameters
    ----------
    color:
        byte array containing 4 bytes

    Returns
    -------
    r:
        Red-value
    g:
        Green-value
    b:
        Blue-value
    a:
        Alpha-value
    """
    return tuple(map(int, color))


def get_rgba_f(color: bytes) -> Tuple[float, ...]:
    """Convert color bytes array into a (r,g,b,a) float-tuple with values [0.0,1.0]

    Parameters
    ----------
    color:
        byte array containing 4 bytes

    Returns
    -------
    r:
        Red-value
    g:
        Green-value
    b:
        Blue-value
    a:
        Alpha-value
    """
    scale = lambda x: x / 255.0
    return tuple(map(scale, color))
