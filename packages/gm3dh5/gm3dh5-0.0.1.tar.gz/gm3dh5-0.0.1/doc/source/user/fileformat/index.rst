.. _fileformat:

##########################
Result File Specifications
##########################

GrainMapper3D Result File Format
--------------------------------

The GrainMapper3D Result File is a `HDF5 File <https://www.hdfgroup.org>`__ 
with groups and datasets specified in the :ref:`specs`. 

Volumetric data is stored as 3D arrays, where the z-dimension comes
first. All datasets confide to the :ref:`coords`.

The (X,Y,Z) coordinates of a dataset's ``Center``, ``Extent``, ``Spacing`` and
``VirtualShift`` are given in millimeter (mm). The ``VirtualShift`` refers
to the motor positions of the sample stage. The ``Center`` refers to the
center of a bounding box given by ``Extent``. The ``Extent`` is subdivided
by *N* voxels along one dimension (i.e., ``Extent`` = ``Spacing`` x *N*).
Several reconstructions of the same sample can be brought into
coincidence using ``Center`` + ``VirtualShift``.

.. _specs:

.. toctree::
   :caption: Result File Specifications
   :maxdepth: 1

   specs/v5
   specs/v4
   specs/v3
   specs/v1
