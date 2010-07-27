.. Adsorption documentation master file, created by
   sphinx-quickstart on Tue Jul 27 14:33:27 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Adsorption's documentation!
======================================

.. toctree::
   :maxdepth: 2

.. contents::

Introduction
------------

Adsorption is a lightweight loose coupling library for Python. It has no
dependencies and can be used with any sort of framework for loose
coupling of components within an application. It was written with web
applications in mind, but makes no assumptions about where or how it
will be used.

Usage
-----

Start with declaring a container for your events. This should ideally
be a singleton for your entire application, so declare it somewhere
that it can be imported from across your app::

  >>> from adsorb import Adsorber
  >>> events = Adsorber()

Declare a listener for an event. Events in Adsorption do not need to be
declared. They exist as long as they have at least one caller or listener::

  >>> @events.listener('event1')
  ... def listener(event):
  ...     print 'Listener received context', repr(event.context)
  ...     return "processed"

  >>> @events.listener('event1')
  ... def listener2(event):
  ...     return "also-processed"

Raise an event from anywhere. Event listeners are called and all responses are
collected before execution resumes with the caller. The order in which
listeners are called is not defined. Listeners are not expected to be
order-aware::

  >>> e = events.raiseEvent('event1', 'some-context')
  Listener received context 'some-context'
  >>> sorted(e.results.items())
  [('__main__.listener', 'processed'), ('__main__.listener2', 'also-processed')]

If a listener raises an exception, the exception is captured in :attr:`Event.exceptions`.
Future versions may add support to call listeners in parallel threads.



API Documentation
-----------------

Package :mod:`adsorb`
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: adsorb.adsorb
   :members: Adsorber, Event

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

