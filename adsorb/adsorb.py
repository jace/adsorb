# -*- coding: utf-8 -*-

from sys import exc_info
from collections import defaultdict

class Event(object):
    """
    Collects responses to the event. Attributes:

    * :attr:`name`: Name of the event
    * :attr:`context`: Context for event, provided by caller
    * :attr:`data`: Additional data provided by caller
    * :attr:`results`: Dictionary of results from each listener
    * :attr:`exceptions`: Dictionary of ``(exception, value)`` from failed listeners

    Event objects are automatically created by :meth:`Adsorber.raiseEvent` and passed
    as the sole parameter to each listener.
    """
    def __init__(self, adsorber, name, context, **kw):
        self.adsorber = adsorber
        self.name = name
        self.context = context
        self.data = kw
        self.results = {}
        self.exceptions = {}

    def __repr__(self):
        return u"<Event '%s'> on %s" % (self.name, repr(self.context))

    def call(self):
        """
        Call all listeners for this event and collect their output.
        """
        events = self.adsorber._getEvents(self.name)
        for listenerid in events:
            try:
                self.results[listenerid] = events[listenerid](self)
            except:
                self.exceptions[listenerid] = exc_info()[:2] # Save exception and value


class Adsorber(object):
    """
    Container for events and listeners. Typically used as a singleton instance
    for the entire application.
    """
    def __init__(self):
        self.__events = defaultdict(dict)

    def _getEvents(self, name):
        """Return all events for given event name."""
        return self.__events[name]

    def addListener(self, eventname, listenerid, listener):
        """
        Add a listener to the named event. Listeners are passed an instance of
        :class:`Event` as the sole parameter. The return value from the listener
        is collected in the event object's :attr:`results` attribute.
        """
        self.__events[eventname][listenerid] = listener

    def removeListener(self, eventname, listenerid):
        """
        Remove a listener on an event.
        """
        del self.__events[eventname][listenerid]

    def removeEvent(self, eventname, confirm=False):
        """
        Remove all listeners on an event.
        """
        if confirm:
            del self.__events[eventname]

    def raiseEvent(self, eventname, context, **kw):
        """
        Raise an event. All listeners are called and their return values or
        exceptions are collected before execution resumes with the caller.
        Caller must provide a mandatory ``context`` and optional named attributes
        as data for the event.
        """
        e = Event(self, eventname, context, **kw)
        e.call()
        return e

    def listener(self, eventname):
        """
        Decorator for event listeners to automate the call to :meth:`addListener`.
        Usage::

            @adsorb_instance.listener("event-name")
            def your_listener(event):
                ...
                
            @adsorb_instance.listener(("event1", event2")):
            def your_listener(event):
                ...

        A listenerid for the listener is automatically constructed from the
        module and function names. This decorator can only be used with module
        top-level functions. For class methods and nested functions, call
        :meth:`addListener` at run-time.
        """
        def decorator(f):
            listenerid = '%s.%s' % (f.__module__, f.__name__)
            if isinstance(eventname, (tuple, list)):
                for e in eventname:
                    self.addListener(e, listenerid, f)
            else:
                self.addListener(eventname, listenerid, f)
            return f
        return decorator
