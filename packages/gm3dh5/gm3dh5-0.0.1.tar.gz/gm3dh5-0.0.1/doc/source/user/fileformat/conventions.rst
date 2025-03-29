.. _coords:

Coordinate System Conventions
=============================

.. _subsec.Axis-Definitions:

Axis Definitions
----------------

The :ref:`AxisZEISS` figure shows how
**SampleX**, **SampleY** and **SampleZ** are defined by
the Scout-and-Scan Control System when the sample is mounted on the
ZEISS Xradia Versa or the ZEISS Xradia CrystalCT and the Sample Theta
stage is at 0°. When the Sample Theta stage is at -90°, **SampleZ**
moves orthogonal to the beam line and **SampleX** moves on the beam
line. This coordinate system is also used by the Acquisition Wizard to
operate the microscope consistently.

.. _AxisZEISS:

.. figure:: zeisscoordinates.svg
   :scale: 150 %

   Scout-and-Scan Coordinate Convention 

Refer to the ZEISS sample axis definitions outlined in the ”Axis
Definitions” in Chapter 1 of the instruments user guide.
GrainMapper3D operates with a relative coordinate system attached to the
imported absorption volume as pictured in :ref:`AxisLabDCT`. 
By default the origin (0,0,0) of the GrainMapper3D coordinate system 
is the mean **SampleX**, **SampleY** and **SampleZ** stage position of 
the reconstructed absorption volume.

.. _AxisLabDCT:
.. figure:: xnovocoordinates.svg
   :scale: 150 %

   GrainMapper3D Coordinate Convention

For a sample coordinate :math:`({x,y,z})` given in one or the other
coordinate system, the transformations are:


.. math::

   \left(\begin{array}{c}
   x\\
   y\\
   z
   \end{array}\right)_{\text{Xnovo}}=\left(\begin{array}{ccc}
   0 & 0 & 1\\
   -1 & 0 & 0\\
   0 & -1 & 0
   \end{array}\right)\left(\begin{array}{c}
   x\\
   y\\
   z
   \end{array}\right)_{\text{ZEISS}}=\left(\begin{array}{c}
   z\\
   -x\\
   -y
   \end{array}\right)_{\text{ZEISS}}

and

.. math::

   \left(\begin{array}{c}
   x\\
   y\\
   z
   \end{array}\right)_{\text{ZEISS}}=\left(\begin{array}{ccc}
   0 & -1 & 0\\
   0 & 0 & -1\\
   1 & 0 & 0
   \end{array}\right)\left(\begin{array}{c}
   x\\
   y\\
   z
   \end{array}\right)_{\text{Xnovo}}=\left(\begin{array}{c}
   -y\\
   -z\\
   x
   \end{array}\right)_{\text{Xnovo}}.


.. _subsec.Crystal-Reference-Frame:

Crystal Reference Frame
-----------------------

The crystal reference frame used is defined according to the
international convention,

.. math:: \mathbf{x} \parallel \mathbf{a},\qquad \mathbf{z} \parallel \mathbf{c}^{*},

which for unit cell parameters :math:`({a,b,c,\alpha,\beta,\gamma})`
results in the direct structure matrix

.. math::

   \text{B} = \begin{pmatrix}
   a & {b\cos\gamma} & {c\cos\beta} \\
   0 & {b\sin\gamma} & {c\csc\gamma\left( {\cos\alpha - \cos\beta\cos\gamma} \right)} \\
   0 & 0 & {c\csc\gamma\sqrt{1 - \cos^{2}\alpha - \cos^{2}\beta - \cos^{2}\gamma + 2\cos\alpha\cos\beta\cos\gamma}}
   \end{pmatrix}

and the reciprocal structure matrix
:math:`\mathbf{B}^{*} = \mathbf{B}^{- 1}`, respectively. A direct space
vector :math:`\mathbf{u} = (u,v,w)^{T}` has the coordinate

.. math:: \mathbf{u}' = \mathbf{B}\mathbf{u}

in the crystal reference frame. A reciprocal lattice vector
:math:`\mathbf{h} = (h,k,l)^{T}` has the coordinate

.. math:: \mathbf{h}'^{T} = \mathbf{h}^{T}\mathbf{B}^{*}

in the crystal reference frame.

.. _subsec.Orientation-Convention:

Orientation Convention
----------------------

The rotation matrix :math:`\mathbf{U}` maps a vector :math:`\mathbf{h}'`
from the crystal reference frame onto a vector :math:`\mathbf{r}` in the
sample reference frame,

.. math:: \mathbf{U}\mathbf{h}' = \mathbf{r},

where the sample reference frame is defined according to the axis
definitions in :ref:`AxisLabDCT`.

.. note::

   For comparison with common post-processing tools for 
   crystallographic data, the GrainMapper3D orientation convention is 
   the same as used by `MTEX <https://mtex-toolbox.github.io/>`__, and
   the inverse of that adapted by `DREAM.3D <http://dream3d.bluequartz.net/>`__.

