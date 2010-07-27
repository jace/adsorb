Adsorption
==========

Lightweight loose coupling library for Python. Add listeners to a named event
and call them from anywhere to collect their responses.

Event listeners are called in an undefined sequence and all responses are
collected before execution resumes with the caller. Future versions may
add support to call listeners in parallel threads.

Installation
------------

Run ``easy_install adsorb`` or ``pip install adsorb`` to get from
`PyPI <http://pypi.python.org/>`__ (not yet implemented).

To install from source, run ``python setup.py install``.

To run the tests, install ``nose`` and ``coverage`` and run
``python setup.py nosetests``.

Usage
-----

See ``docs/``
