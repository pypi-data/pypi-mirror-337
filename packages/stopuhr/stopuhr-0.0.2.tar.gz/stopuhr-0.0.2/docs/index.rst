.. stopuhr documentation master file, created by
   sphinx-quickstart on Thu mar 27 19:28:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#########################################
Welcome to stopuhr's documentation!
#########################################

**Version**: |version|

A simple tool for measuring durations in Python.

.. toctree::
   :maxdepth: 1

   Reference <reference/index>
   Examples <auto_examples/index>

Quick Start
===========

Installation
------------

You can install stopuhr via pip:

.. code-block:: bash

    pip install stopuhr

However, `uv` is recommended for installing python packages:

.. code-block:: bash

    uv add stopuhr

Usage
-----

With stopuhr it is convinient to measure durations in Python:

.. code-block:: python

    from stopuhr import stopuhr

    with stopuhr("My Timer"):
        # Do something
        pass

For a stateful version, a decorator or a stateful decorator please visit the Reference or have a look at the examples.
