Overview
========

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.15110079.svg
  :target: https://doi.org/10.5281/zenodo.15110079

The module computes various polynomials useful for `webnucleo <https://webnucleo.readthedocs.io>`_ projects.  In particular, the package has modules to compute symmetric and Bell polynomials for input sets of variables.  For the complete Bell polynomials, the package also has a routine to invert an appropriate set of Bell polynomials to find the variables that would give rise to those polynomials.

|pypi| |doc_stat| |license| |test| |lint-test| |black|

Installation
------------

Install from `PyPI <https://pypi.org/project/wnpoly>`_ with pip by
typing in your favorite terminal::

    $ pip install wnpoly

Usage
-----

To learn how to use the package, follow the Jupyter notebook
`tutorial <https://github.com/mbradle/wnpoly/blob/main/tutorial/>`_.

Authors
-------

- Bradley S. Meyer <mbradle@g.clemson.edu>
- Ian Reistroffer <ireistr@g.clemson.edu>

Contribute
----------

- Issue Tracker: `<https://github.com/mbradle/wnpoly/issues/>`_
- Source Code: `<https://github.com/mbradle/wnpoly/>`_

License
-------

The project is licensed under the GNU Public License v3 (or later).

Documentation
-------------

The project documentation is available at `<https://wnpoly.readthedocs.io>`_.

.. |pypi| image:: https://badge.fury.io/py/wnpoly.svg 
    :target: https://badge.fury.io/py/wnpoly
.. |license| image:: https://img.shields.io/github/license/mbradle/wnpoly
    :alt: GitHub
.. |doc_stat| image:: https://readthedocs.org/projects/wnpoly/badge/?version=latest 
    :target: https://wnpoly.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |test| image:: https://github.com/mbradle/wnpoly/actions/workflows/test.yml/badge.svg?branch=main&event=push
        :target: https://github.com/mbradle/wnpoly/actions/workflows/test.yml
.. |lint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint
.. |lint-test| image:: https://github.com/mbradle/wnpoly/actions/workflows/lint.yml/badge.svg?branch=main&event=push
        :target: https://github.com/mbradle/wnpoly/actions/workflows/lint.yml
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
