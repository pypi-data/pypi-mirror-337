Installation Instructions
=========================

Let's see how to install AQC-Tensor. The first
thing to do is choose how you're going to run and install the
packages. There are two primary ways to do this:

- :ref:`Option 1`
- :ref:`Option 2`

Pre-Installation
^^^^^^^^^^^^^^^^

Users who wish to install locally (using either :ref:`Option 1` or :ref:`Option 2`) are encouraged to
follow a brief set of common instructions to prepare a Python environment for
installation of AQC-Tensor:

First, create a minimal environment with only Python installed in it. We recommend using `Python virtual environments <https://docs.python.org/3.10/tutorial/venv.html>`__.

.. code:: sh

    python3 -m venv /path/to/virtual/environment

Activate your new environment.

.. code:: sh

    source /path/to/virtual/environment/bin/activate

Note: If you are using Windows, use the following commands in PowerShell:

.. code:: pwsh

    python3 -m venv c:\path\to\virtual\environment
    c:\path\to\virtual\environment\Scripts\Activate.ps1


.. _Option 1:

Option 1: Pip Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Upgrade pip and install the AQC-Tensor package.  To meaningfully use the package, you must also install at least one tensor network backend.  The below snippet installs the addon, along with quimb (for tensor network support) and jax (for automatic differentiation).

.. code:: sh

    pip install --upgrade pip
    pip install qiskit-addon-aqc-tensor[quimb-jax]


.. _Option 2:

Option 2: Install from Source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users who wish to develop in the repository or run the tutorials locally may want to install from source.

In either case, the first step is to clone the AQC-Tensor repository.

.. code:: sh

    git clone git@github.com:Qiskit/qiskit-addon-aqc-tensor.git

Next, upgrade pip and enter the repository.

.. code:: sh

    pip install --upgrade pip
    cd qiskit-addon-aqc-tensor

The next step is to install AQC-Tensor to the virtual environment. If you plan on running the tutorials, install the
notebook dependencies in order to run all the visualizations in the notebooks.
If you plan on developing in the repository, you may want to install the ``dev`` dependencies.

Adjust the options below to suit your needs.

.. code:: sh

    pip install tox jupyterlab -e '.[notebook-dependencies,dev]'

If you installed the notebook dependencies, you can get started with AQC-Tensor by running the notebooks in the docs.

.. code::

    cd docs/
    jupyter lab


.. _Platform Support:

Platform Support
^^^^^^^^^^^^^^^^

We expect this package to work on `any Tier 1 platform supported by Qiskit <https://docs.quantum.ibm.com/start/install#operating-system-support>`__.
