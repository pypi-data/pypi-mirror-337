============
Installation
============

gm3dh5 is listed in the `Python Package Index <https://pypi.python.org/pypi>`__. 
Therefore, it can be automatically downloaded and installed with `pip <https://pypi.python.org/pypi/pip>`__.
You may need to install pip for the following commands to run.

From pip
--------

To install gm3dh5 from pip, run::

    pip install gm3dh5

or use::

    python -m pip install gm3dh5

To update gm3dh5 to the latest release::

    pip install --upgrade gm3dh5

To install a specific version of gm3dh5 (say version 0.0.1)::

    pip install gm3dh5==0.0.1

In case you want to enable additional features use::

    pip install gm3dh5[numba]"



From source
-----------

To install gm3dh5 from source, clone the repository from `GitHub
<https://github.com/xnovotech/gm3dh5>`__, and install with ``pip``::


    git clone https://github.com/xnovotech/gm3dh5.git
    cd gm3dh5
    pip install --editable .

The software has optional dependencies for some functionality.
See the tables below for the core and optional dependencies.
To install all dependencies, do:

.. code-block:: bash

    pip install ".[numba,doc]"


Dependencies
------------

This is a list of package dependencies:

* :doc:`h5py <h5py:index>`: HDF5 file support.
* :doc:`numpy <numpy:index>`: Handling of N-dimensional arrays (optional)

Some functionality requires optional dependencies:

* :doc:`numba <numba:index>`: CPU acceleration
