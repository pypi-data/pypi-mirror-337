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
from typing import Tuple, Union, overload

import numpy as np

from .types import ArrayLike, ArrayNoneLike, BoolArrayLike, NDArray
from .vec3 import Vec3

__all__ = ["Quaternion"]


class Quaternion:
    """
    A class for representation and calculation of quaternions.
    """

    def __init__(
        self,
        a: Union["Quaternion", ArrayNoneLike] = None,
        b: ArrayNoneLike = None,
        c: ArrayNoneLike = None,
        d: ArrayNoneLike = None,
    ):
        if b is None and c is None and d is None:
            if isinstance(a, (np.ndarray, np.generic)):
                assert a.shape[0] == 4, "Expected shape (4,...)"
                b, c, d, a = a[1], a[2], a[3], a[0]
            elif isinstance(a, Quaternion):
                b, c, d, a = a.b, a.c, a.d, a.a

        self.a: np.ndarray = np.asarray(a, dtype=float)
        self.b: np.ndarray = np.asarray(b, dtype=float)
        self.c: np.ndarray = np.asarray(c, dtype=float)
        self.d: np.ndarray = np.asarray(d, dtype=float)

        # late throw
        assert (
            self.a.shape == self.b.shape
            and self.b.shape == self.c.shape
            and self.c.shape == self.d.shape
        ), "All vectors must be of equal size"

    @classmethod
    def concatenate(cls, tup, **kwargs):
        assert all(isinstance(q, Quaternion) for q in tup), (
            "Expected Quaternions as input"
        )

        a = np.concatenate(tuple(q.a for q in tup), **kwargs)
        b = np.concatenate(tuple(q.b for q in tup), **kwargs)
        c = np.concatenate(tuple(q.c for q in tup), **kwargs)
        d = np.concatenate(tuple(q.d for q in tup), **kwargs)
        return cls(a, b, c, d)

    @classmethod
    def stack(cls, tup, **kwargs):
        assert all(isinstance(q, Quaternion) for q in tup), (
            "Expected Quaternions as input"
        )

        a = np.stack(tuple(q.a for q in tup), **kwargs)
        b = np.stack(tuple(q.b for q in tup), **kwargs)
        c = np.stack(tuple(q.c for q in tup), **kwargs)
        d = np.stack(tuple(q.d for q in tup), **kwargs)
        return cls(a, b, c, d)

    @classmethod
    def vstack(cls, tup, **kwargs):
        assert all(isinstance(q, Quaternion) for q in tup), (
            "Expected Quaternions as input"
        )

        a = np.vstack(tuple(q.a for q in tup), **kwargs)
        b = np.vstack(tuple(q.b for q in tup), **kwargs)
        c = np.vstack(tuple(q.c for q in tup), **kwargs)
        d = np.vstack(tuple(q.d for q in tup), **kwargs)
        return cls(a, b, c, d)

    @classmethod
    def hstack(cls, tup, **kwargs):
        assert all(isinstance(q, Quaternion) for q in tup), (
            "Expected Quaternions as input"
        )

        a = np.hstack(tuple(q.a for q in tup), **kwargs)
        b = np.hstack(tuple(q.b for q in tup), **kwargs)
        c = np.hstack(tuple(q.c for q in tup), **kwargs)
        d = np.hstack(tuple(q.d for q in tup), **kwargs)
        return cls(a, b, c, d)

    @classmethod
    def from_axis_angle(cls, axis: Vec3, angle: ArrayLike):
        """Initializes quaternion from axis-angle.

        Parameters
        ----------
        axis
            Rotation axis given as Vec3
        angle
            Rotation angle in radians

        Returns
        -------
            Quaternion
        """
        assert isinstance(axis, Vec3), "Expected Vec3"

        n = axis.norm()
        isnotzero = np.logical_not(np.isclose(n, 0))  # tolerances?
        ax = Vec3.like(axis)
        ax[isnotzero] = axis[isnotzero] / n[isnotzero]

        halfAngle = angle / 2.0
        a = np.cos(halfAngle)
        qv = ax * np.sin(halfAngle)
        return cls(a, qv.x, qv.y, qv.z)

    @classmethod
    def from_rodrigues(cls, rod: Vec3):
        """Initializes quaternion from Rodrigues vector.

        Parameters
        ----------
        rod
            Rodrigues vector as a list

        Returns
        -------
            Quaternion
        """
        assert isinstance(rod, Vec3), "Expected Vec3"
        return cls.from_axis_angle(rod, 2.0 * np.arctan(rod.norm()))

    @classmethod
    def from_rotation_matrix(cls, rm: NDArray):
        """Initialises from rotation matrix.
        This code is more or less taken from
        http://www.martinb.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm.

        Parameters
        ----------
        rm
            Rotation matrix to initialze from.

        Returns
        -------
            Quaternion
        """
        trace = np.trace(rm)
        # preallocate
        a = np.zeros((rm.shape[2:]))
        b = np.zeros((rm.shape[2:]))
        c = np.zeros((rm.shape[2:]))
        d = np.zeros((rm.shape[2:]))

        t0 = trace > 0
        t1 = (rm[0, 0] > rm[1, 1]) & (rm[0, 0] > rm[2, 2])
        t2 = rm[1, 1] > rm[2, 2]
        t3 = ~(t0 | t1 | t2)

        # fmt: off

        if np.any(t0):
            _s = np.sqrt(trace[t0] + 1.)
            s = 2. * _s
            a[t0] = _s / 2.0 #(s/4)
            b[t0] = (rm[2, 1,t0] - rm[1, 2,t0]) / s
            c[t0] = (rm[0, 2,t0] - rm[2, 0,t0]) / s
            d[t0] = (rm[1, 0,t0] - rm[0, 1,t0]) / s

        if np.any(t1):
            _s = np.sqrt(1.0 + rm[0, 0,t1] - rm[1, 1,t1] - rm[2, 2,t1])
            s = 2.0 *_s
            b[t1] = _s / 2.0
            c[t1] = (rm[0, 1,t1] + rm[1, 0,t1]) / s
            d[t1] = (rm[0, 2,t1] + rm[2, 0,t1]) / s
            a[t1] = (rm[2, 1,t1] - rm[1, 2,t1]) / s

        if np.any(t2):
            _s = np.sqrt(1.0 + rm[1, 1,t2] - rm[0, 0,t2] - rm[2, 2,t2])
            s = 2.0 *_s
            b[t2] = (rm[0, 1,t2] + rm[1, 0,t2]) / s
            c[t2] = _s / 2.0
            d[t2] = (rm[1, 2,t2] + rm[2, 1,t2]) / s
            a[t2] = (rm[0, 2,t2] - rm[2, 0,t2]) / s

        if np.any(t3):
            _s = np.sqrt(1.0 + rm[2, 2,t3] - rm[0, 0,t3] - rm[1, 1,t3])
            s = 2.0*_s
            b[t3] = (rm[0, 2,t3] + rm[2, 0,t3]) / s
            c[t3] = (rm[1, 2,t3] + rm[2, 1,t3]) / s
            d[t3] = _s/2.0
            a[t3] = (rm[1, 0,t3] - rm[0, 1,t3]) / s
        # fmt: on

        return cls(a, b, c, d)

    @classmethod
    def like(cls, other: "Quaternion"):
        return cls(
            np.zeros_like(other.a),
            np.zeros_like(other.b),
            np.zeros_like(other.c),
            np.zeros_like(other.d),
        )

    @classmethod
    def rand(cls, *args):
        """Return a sample (or samples) from the uniform spherical quaternion distribution.

        Example
        -------
        >>> Quaternion.rand(d0,d1,...,dn)
        """

        alpha = 2.0 * np.pi * (np.random.rand(*args) - 0.5)
        beta = np.arccos(2.0 * np.random.rand(*args) - 1)
        gamma = 2.0 * np.pi * (np.random.rand(*args) - 0.5)

        return cls.from_euler_abg(alpha, beta, gamma)

    @classmethod
    def zeros(cls, *args):
        return cls(
            np.zeros(*args),
            np.zeros(*args),
            np.zeros(*args),
            np.zeros(*args),
        )

    @classmethod
    def identity(cls, *args):
        return cls(
            np.ones(*args),
            np.zeros(*args),
            np.zeros(*args),
            np.zeros(*args),
        )

    @classmethod
    def nan(cls, shape):
        return cls(
            np.full(shape, np.nan),
            np.full(shape, np.nan),
            np.full(shape, np.nan),
            np.full(shape, np.nan),
        )

    def isnan(self):
        return np.isnan(self.a) | np.isnan(self.b) | np.isnan(self.c) | np.isnan(self.d)

    @classmethod
    def from_euler_abg(cls, alpha, beta, gamma):
        return cls.from_euler_zyz(alpha, beta, gamma)

    @classmethod
    def from_euler_bunge(cls, phi1, Phi, phi2):
        return cls.from_euler_zxz(phi1, Phi, phi2)

    @classmethod
    def from_rot_x(cls, w):
        whalf = w / 2.0
        z = np.zeros_like(w)
        return cls(np.cos(whalf), np.sin(whalf), z, z)

    @classmethod
    def from_rot_y(cls, w):
        whalf = w / 2.0
        z = np.zeros_like(w)
        return cls(np.cos(whalf), z, np.sin(whalf), z)

    @classmethod
    def from_rot_z(cls, w):
        whalf = w / 2.0
        z = np.zeros_like(w)
        return cls(np.cos(whalf), z, z, np.sin(whalf))

    @classmethod
    def from_euler_zyz(cls, alpha, beta, gamma):
        return (
            Quaternion.from_rot_z(alpha)
            * Quaternion.from_rot_y(beta)
            * Quaternion.from_rot_z(gamma)
        )

    @classmethod
    def from_euler_zxz(cls, phi1, Phi, phi2):
        return (
            Quaternion.from_rot_z(phi1)
            * Quaternion.from_rot_x(Phi)
            * Quaternion.from_rot_z(phi2)
        )

    def __iter__(self):
        for a, b, c, d in zip(self.a, self.b, self.c, self.d):
            yield Quaternion(a, b, c, d)

    def __getitem__(self, subs):
        return Quaternion(self.a[subs], self.b[subs], self.c[subs], self.d[subs])

    def __setitem__(self, subs, value):
        if isinstance(value, Quaternion):
            self.a[subs] = value.a
            self.b[subs] = value.b
            self.c[subs] = value.c
            self.d[subs] = value.d
        else:
            raise TypeError(value)

    def norm(self) -> ArrayLike:
        return np.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

    def normalize(self):
        n = self.norm()
        assert np.all(~np.isclose(n, 0)), "Cannot normalise quaternion(0,0,0,0)"
        return Quaternion(self.a / n, self.b / n, self.c / n, self.d / n)

    def inv(self) -> "Quaternion":
        n = self.a**2 + self.b**2 + self.c**2 + self.d**2
        assert np.all(n[np.isfinite(n)] > 0), (
            "The inverse of quaternion(0,0,0,0) is not defined"
        )
        return Quaternion(self.a / n, -self.b / n, -self.c / n, -self.d / n)

    def conj(self) -> "Quaternion":
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def dot(self, other: "Quaternion") -> ArrayLike:
        assert isinstance(other, Quaternion), "Expected Vec3"
        return self.a * other.a + self.b * other.b + self.c * other.c + self.d * other.d

    def angle(self, other=None) -> ArrayLike:
        d = (
            np.abs(self.dot(other))
            if isinstance(other, Quaternion)
            else np.array(np.abs(self.a))
        )
        s = d < 1
        if d.size == 1:
            return 2.0 * np.arccos(d) if s else 0
        else:
            d[s] = 2.0 * np.arccos(d[s])
            d[~s] = 0
            return d

    def axis(self) -> Vec3:
        v = Vec3(self.b, self.c, self.d)

        i = self.a < 0.0
        v[i] = -v[i]
        n = v.norm()
        i = np.isclose(n, 0)
        v[i] = Vec3(1.0, 0.0, 0.0)
        i = np.logical_not(i)
        v[i] = v[i] / n[i]  # normalize

        return v

    def isfinite(self) -> BoolArrayLike:
        return (
            np.isfinite(self.a)
            & np.isfinite(self.b)
            & np.isfinite(self.c)
            & np.isfinite(self.d)
        )

    # Return corresponding Rodrigues vector
    def as_rodrigues(self) -> Vec3:
        return Vec3(self.b / self.a, self.c / self.a, self.d / self.a)

    def as_rotation_matrix(self) -> np.ndarray:
        a, b, c, d = self.a, self.b, self.c, self.d
        a11 = 1 - 2 * c**2 - 2 * d**2
        a12 = 2 * b * c - 2 * d * a
        a13 = 2 * b * d + 2 * c * a

        a21 = 2 * b * c + 2 * d * a
        a22 = 1 - 2 * b**2 - 2 * d**2
        a23 = 2 * c * d - 2 * b * a

        a31 = 2 * b * d - 2 * c * a
        a32 = 2 * c * d + 2 * b * a
        a33 = 1 - 2 * b**2 - 2 * c**2

        return np.stack(
            [
                [a11, a12, a13],
                [a21, a22, a23],
                [a31, a32, a33],
            ]
        )

    def as_euler_zxz(self) -> Tuple[ArrayLike, ArrayLike, ArrayLike]:
        [alpha, beta, gamma] = self.as_euler_zyz()

        ind = np.logical_not(np.isclose(beta, 0))
        if np.isscalar(ind) and ind:
            alpha = alpha + np.pi / 2.0
            gamma = gamma + 3 * np.pi / 2.0
        elif np.any(ind):
            alpha[ind] = alpha[ind] + np.pi / 2.0
            gamma[ind] = gamma[ind] + 3 * np.pi / 2.0

        # necessary?
        alpha = np.mod(alpha, 2 * np.pi)
        gamma = np.mod(gamma, 2 * np.pi)

        return alpha, beta, gamma

    def as_euler_zyz(self) -> Tuple[ArrayLike, ArrayLike, ArrayLike]:
        def ssign(val):
            ret = np.ones_like(val)
            ret[val < 0] = -1
            return ret

        at1 = np.arctan2(self.d, self.a)
        at2 = np.arctan2(self.b, self.c)

        alpha = at1 - at2
        beta = 2 * np.arctan2(
            np.sqrt(self.b**2 + self.c**2), np.sqrt(self.a**2 + self.d**2)
        )
        gamma = at1 + at2

        ind = np.isclose(beta, 0)
        if np.isscalar(ind) and ind:
            alpha = 2 * np.arcsin(np.clip(ssign(self.a) * self.d, -1, 1))
            gamma = 0.0
        elif np.any(ind):
            alpha[ind] = 2 * np.arcsin(np.clip(ssign(self.a[ind]) * self.d[ind], -1, 1))
            gamma[ind] = 0.0

        return alpha, beta, gamma

    def as_euler_bunge(self) -> Tuple[ArrayLike, ArrayLike, ArrayLike]:
        return self.as_euler_zxz()

    def as_euler_abg(self) -> Tuple[ArrayLike, ArrayLike, ArrayLike]:
        return self.as_euler_zyz()

    def aslist(self) -> list:
        return [self.a, self.b, self.c, self.d]

    def asarray(self) -> ArrayLike:
        return np.array(self.aslist())

    def __eq__(self, other) -> BoolArrayLike:
        if isinstance(other, Quaternion):
            if self.shape != other.shape:
                return False
            else:
                return (
                    (self.a == other.a)
                    & (self.b == other.b)
                    & (self.c == other.c)
                    & (self.d == other.d)
                )
        return False

    def __ne__(self, other) -> BoolArrayLike:
        return np.logical_not(self == other)

    def __neg__(self) -> "Quaternion":
        return Quaternion(-self.a, -self.b, -self.c, -self.d)

    @overload
    def __mul__(self, other: Vec3) -> Vec3: ...

    @overload
    def __mul__(self, other: "Quaternion") -> "Quaternion": ...

    def __mul__(self, other):
        # fmt: off
        if isinstance(other, Quaternion):  
            return Quaternion(
                self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d,
                self.a * other.b + other.a * self.b - self.d * other.c + self.c * other.d,
                self.a * other.c + other.a * self.c - self.b * other.d + self.d * other.b,
                self.a * other.d + other.a * self.d + self.b * other.c - self.c * other.b
            )
        elif isinstance(other,Vec3):
            tx = 2.0 * (self.c * other.z - self.d * other.y)
            ty = 2.0 * (self.d * other.x - self.b * other.z)
            tz = 2.0 * (self.b * other.y - self.c * other.x)

            return Vec3(
                other.x + self.a * tx - self.d * ty + self.c * tz,
                other.y + self.d * tx + self.a * ty - self.b * tz,
                other.z - self.c * tx + self.b * ty + self.a * tz
            )
        elif isinstance(other, (Number,np.ndarray, np.generic)):  
            return Quaternion(self.a * other, self.b * other,self.c * other, self.d * other)  
        else:
            raise TypeError(other)
        # fmt: on

    def reshape(self, *args, **kwargs):
        return Quaternion(
            self.a.reshape(*args, **kwargs),
            self.b.reshape(*args, **kwargs),
            self.c.reshape(*args, **kwargs),
            self.d.reshape(*args, **kwargs),
        )

    def flatten(self, **kwargs):
        return Quaternion(
            self.a.flatten(**kwargs),
            self.b.flatten(**kwargs),
            self.c.flatten(**kwargs),
            self.d.flatten(**kwargs),
        )

    def ravel(self, **kwargs):
        return Quaternion(
            self.a.ravel(**kwargs),
            self.b.ravel(**kwargs),
            self.c.ravel(**kwargs),
            self.d.ravel(**kwargs),
        )

    @property
    def ndim(self) -> int:
        return self.a.ndim

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.a.shape

    @shape.setter
    def shape(self, shape):
        self.a.shape = shape
        self.b.shape = shape
        self.c.shape = shape
        self.d.shape = shape

    @property
    def size(self) -> int:
        return self.a.size

    def __str__(self) -> str:
        f = lambda x: np.array2string(x, prefix="   ")
        if self.a.size > 1:
            return (
                f"Quaternion<{self.shape}>(\n"
                f" a={f(self.a)},\n"
                f" b={f(self.b)},\n"
                f" c={f(self.c)},\n"
                f" d={f(self.d)}\n)"
            )
        else:
            return f"Quaternion({f(self.a)},{f(self.b)},{f(self.c)},{f(self.d)})"

    def __repr__(self):
        return str(self)
