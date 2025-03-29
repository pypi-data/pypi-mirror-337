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

from numbers import Number
from typing import Tuple, Union

import numpy as np

from .types import ArrayLike, ArrayNoneLike, BoolArrayLike, NDArray

__all__ = ["Vec3"]


class Vec3:
    def __init__(
        self,
        x: Union["Vec3", ArrayNoneLike] = None,
        y: ArrayNoneLike = None,
        z: ArrayNoneLike = None,
    ) -> None:
        if y is None and z is None:
            if isinstance(x, (np.ndarray, np.generic)):
                assert x.shape[0] == 3, "Expected shape (3,...)"
                y, z, x = x[1], x[2], x[0]
            elif isinstance(x, Vec3):
                y, z, x = x.y, x.z, x.x

        self.x: np.ndarray = np.asarray(x, dtype=float)
        self.y: np.ndarray = np.asarray(y, dtype=float)
        self.z: np.ndarray = np.asarray(z, dtype=float)

        # late throw
        assert self.x.shape == self.y.shape and self.y.shape == self.z.shape, (
            "All vectors must be of equal size"
        )

    @classmethod
    def from_polar_coordinates(
        cls,
        polar: ArrayLike,
        azimuth: ArrayLike,
    ):
        sp = np.sin(polar)
        return cls(sp * np.cos(azimuth), sp * np.sin(azimuth), np.cos(polar))

    @classmethod
    def like(cls, other: "Vec3"):
        return cls(
            np.zeros_like(other.x),
            np.zeros_like(other.y),
            np.zeros_like(other.z),
        )

    @classmethod
    def zeros(cls, *args):
        return cls(np.zeros(args), np.zeros(args), np.zeros(args))

    @classmethod
    def rand(cls, *args):
        """
        Vec3.rand(d0, d1, ..., dn)

        Return a sample (or samples) from the uniform spherical distribution.
        """
        polar = np.arccos(2.0 * np.random.rand(*args) - 1)
        azimuth = 2 * np.pi * (np.random.rand(*args) - 0.5)
        return cls.from_polar_coordinates(polar, azimuth)

    def __iter__(self):
        for x, y, z in zip(self.x, self.y, self.z, strict=True):
            yield Vec3(x, y, z)

    def __getitem__(self, subs):
        return Vec3(self.x[subs], self.y[subs], self.z[subs])

    def __setitem__(self, subs, value):
        if isinstance(value, Vec3):
            self.x[subs] = value.x
            self.y[subs] = value.y
            self.z[subs] = value.z
        else:
            raise TypeError(value)

    def __eq__(self, other: "Vec3") -> BoolArrayLike:
        if isinstance(other, Vec3):
            return (self.x == other.x) & (self.y == other.y) & (self.z == other.z)
        return False

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __neg__(self) -> "Vec3":
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (Number, np.ndarray, np.generic)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(other)

    def __rmul__(self, other) -> "Vec3":
        return self * other

    def __truediv__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, (Number, np.ndarray, np.generic)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(other)

    def __rtruediv__(self, other) -> "Vec3":
        if isinstance(other, (Number, np.ndarray, np.generic)):
            return Vec3(other / self.x, other / self.y, other / self.z)
        else:
            raise TypeError(other)

    def __add__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (Number, np.ndarray, np.generic)):
            return Vec3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError(other)

    def __radd__(self, other) -> "Vec3":
        return self + other

    def __sub__(self, other) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (Number, np.ndarray, np.generic)):
            return Vec3(self.x - other, self.y - other, self.z - other)
        else:
            raise TypeError(other)

    def __rsub__(self, other) -> "Vec3":
        if isinstance(other, (Number, np.ndarray, np.generic)):
            return Vec3(other - self.x, other - self.y, other - self.z)
        else:
            raise TypeError(other)

    def aslist(self) -> list:
        return [self.x, self.y, self.z]

    def asarray(self) -> NDArray:
        return np.asarray(self.aslist())

    def norm(self) -> NDArray:
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> "Vec3":
        return self / self.norm()

    @classmethod
    def concatenate(cls, tup, **kwargs):
        assert all(isinstance(v, Vec3) for v in tup), "Expected Vec3 as input"
        x = np.concatenate(tuple(v.x for v in tup), **kwargs)
        y = np.concatenate(tuple(v.y for v in tup), **kwargs)
        z = np.concatenate(tuple(v.z for v in tup), **kwargs)
        return cls(x, y, z)

    @classmethod
    def stack(cls, tup, **kwargs):
        assert all(isinstance(v, Vec3) for v in tup), "Expected Vec3 as input"
        x = np.stack(tuple(v.x for v in tup), **kwargs)
        y = np.stack(tuple(v.y for v in tup), **kwargs)
        z = np.stack(tuple(v.z for v in tup), **kwargs)
        return cls(x, y, z)

    @classmethod
    def vstack(cls, tup, **kwargs):
        assert all(isinstance(v, Vec3) for v in tup), "Expected Vec3 as input"
        x = np.vstack(tuple(v.x for v in tup), **kwargs)
        y = np.vstack(tuple(v.y for v in tup), **kwargs)
        z = np.vstack(tuple(v.z for v in tup), **kwargs)
        return Vec3(x, y, z)

    @classmethod
    def hstack(cls, tup, **kwargs):
        assert all(isinstance(v, Vec3) for v in tup), "Expected Vec3 as input"
        x = np.hstack(tuple(v.x for v in tup), **kwargs)
        y = np.hstack(tuple(v.y for v in tup), **kwargs)
        z = np.hstack(tuple(v.z for v in tup), **kwargs)
        return cls(x, y, z)

    def reshape(self, *shape, **kwargs):
        return Vec3(
            self.x.reshape(*shape, **kwargs),
            self.y.reshape(*shape, **kwargs),
            self.z.reshape(*shape, **kwargs),
        )

    def flatten(self, **kwargs):
        return Vec3(
            self.x.flatten(**kwargs),
            self.y.flatten(**kwargs),
            self.z.flatten(**kwargs),
        )

    def ravel(self, **kwargs):
        return Vec3(
            self.x.ravel(**kwargs),
            self.y.ravel(**kwargs),
            self.z.ravel(**kwargs),
        )

    def transpose(self):
        """Return transposed shape of array, note only works for 2-D arrays, e.g. used v[np.newaxis]."""
        return Vec3(self.x.transpose(), self.y.transpose(), self.z.transpose())

    @property
    def T(self):
        return self.transpose()

    @property
    def ndim(self) -> int:
        return self.x.ndim

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.x.shape

    @shape.setter
    def shape(self, shape):
        self.x.shape = shape
        self.y.shape = shape
        self.z.shape = shape

    @property
    def size(self) -> int:
        return self.x.size

    def dot(self, other: "Vec3") -> NDArray:
        assert isinstance(other, Vec3), "Expected Vec3"
        return self.x * other.x + self.y * other.y + self.z * other.z  # np.array

    def angle(self, other: "Vec3"):
        assert isinstance(other, Vec3), "Expected Vec3"
        # assert np.all(~np.isclose(a*b),0)),"Cannot normalise quaternion(0,0,0,0)"

        n = self.norm() * other.norm()
        d = self.dot(other)
        ic = ~np.isclose(n, 0)

        if n.size == 1:
            d = d / n if ic else 0
            if d < -1:
                d = -1
            if d > 1:
                d = 1
        else:
            d[ic] = d[ic] / n[ic]
            d[d < -1] = -1
            d[1 < d] = 1
        return np.arccos(d)

    def polar(self):
        return np.arccos(self.z / self.norm())

    def azimuth(self):
        return np.arctan2(self.y, self.x)

    def reflect(self, normal):
        eta = 2 * self.dot(normal)
        return self - normal * eta

    def cross(self, other: "Vec3"):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def isfinite(self):
        return np.isfinite(self.x) & np.isfinite(self.y) & np.isfinite(self.z)

    def isnull(self, eps=None):
        if eps is None:
            eps = np.finfo(float).eps
        return self.norm() < eps

    def round(self, decimals=0):
        return Vec3(
            np.round(self.x, decimals),
            np.round(self.y, decimals),
            np.round(self.z, decimals),
        )

    def orth(self):
        v = Vec3(-self.y, self.x, np.zeros_like(self.x))
        v.x[np.abs(v.y) < np.finfo(float).eps] = 1
        return v

    def antipode(self):  # always upper
        v = Vec3(self)
        ic = self.z < 0
        v[ic] = -v[ic]
        return v

    def __str__(self) -> str:
        if self.x.size > 1:
            f = lambda x: np.array2string(x, prefix="   ")
            return (
                f"Vec3<{self.shape}>(\n"
                f" x={f(self.x)},\n"
                f" y={f(self.y)},\n"
                f" z={f(self.z)},\n)"
            )
        else:
            return f"Vec3({self.x},{self.y},{self.z})"

    def __repr__(self):
        return str(self)
