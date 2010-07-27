# -*- coding: utf-8 -*-

import unittest
from .adsorb import Adsorber

class EventException(Exception):
    pass

class TestEvents(unittest.TestCase):
    def setUp(self):
        self.events = Adsorber()

    def listener1(self, event):
        self.assertTrue(event.name in ['e1', 'e3'])
        return 1

    def listener2(self, event):
        self.assertTrue(event.name in ['e1', 'e2'])
        return 2

    def listener3(self, event):
        self.assertEqual(event.name, 'e2')
        self.assertEqual(event.context, 'context-marker')
        return 3

    def listener4(self, event):
        raise EventException, "test-exception"

    def test_single(self):
        self.events.addListener('e1', 'l1', self.listener1)
        e = self.events.raiseEvent('e1', None)
        self.assertEqual(e.results.get('l1'), 1)
        self.events.removeListener('e1', 'l1')
        e = self.events.raiseEvent('e1', None)
        self.assertEqual(e.results, {})
        self.assertEqual(e.exceptions, {})
        self.assertEqual(repr(e), "<Event 'e1'> on None") # Just to get 100% test coverage

    def test_multi(self):
        self.events.addListener('e1', 'l1', self.listener1)
        self.events.addListener('e1', 'l2', self.listener2)
        self.events.addListener('e2', 'l2', self.listener2)
        self.events.addListener('e2', 'l3', self.listener3)

        e1 = self.events.raiseEvent('e1', None)
        e2 = self.events.raiseEvent('e2', 'context-marker')

        self.assertEqual(set(e1.results.items()), set([('l1', 1), ('l2', 2)]))
        self.assertEqual(set(e2.results.items()), set([('l2', 2), ('l3', 3)]))
        self.assertEqual(e1.exceptions, {})
        self.assertEqual(e2.exceptions, {})

        self.events.removeListener('e1', 'l1')
        self.events.removeListener('e1', 'l2')
        self.events.removeListener('e2', 'l2')
        self.events.removeListener('e2', 'l3')

    def test_exception(self):
        self.events.addListener('e3', 'l1', self.listener1)
        self.events.addListener('e3', 'l4', self.listener4)
        e = self.events.raiseEvent('e3', None)
        self.assertTrue('l1' in e.results)
        self.assertTrue('l4' in e.exceptions)
        self.assertEqual(e.exceptions['l4'][0], EventException)
        self.assertEqual(e.exceptions['l4'][1].args, ('test-exception',))
        self.events.removeListener('e3', 'l1')
        self.events.removeListener('e3', 'l4')

    def test_remove(self):
        self.events.addListener('e3', 'l1', self.listener1)
        self.events.addListener('e3', 'l4', self.listener4)
        self.assertTrue(self.events._getEvents('e3') != {})
        self.events.removeEvent('e3')
        self.assertTrue(self.events._getEvents('e3') != {})
        self.events.removeEvent('e3', confirm=True)
        self.assertTrue(self.events._getEvents('e3') == {})

    def test_decorator(self):
        # Using decorators for nested functions is discouraged, but only
        # because of the potential for listenerid conflicts and for the
        # listener being permanently remembered without garbage collection.
        #
        # It should be fine for a short-lived test suite.
        # DO NOT DO THIS IN PRODUCTION CODE!
        @self.events.listener('e4')
        def decoratedlistener(event):
            return "passed"
        
        e = self.events.raiseEvent('e4', None)
        self.assertEqual(len(e.results), 1)
        self.assertEqual(e.results.values()[0], "passed")
        
        @self.events.listener(('e4', 'e5'))
        def duallistener(event):
            self.assertTrue(event.context in ['call4', 'call5'])
            return 'dual-marker'
            
        e = self.events.raiseEvent('e4', 'call4')
        self.assertEqual(len(e.results), 2)
        self.assertTrue('passed' in e.results.values())
        self.assertTrue('dual-marker' in e.results.values())
        
        e = self.events.raiseEvent('e5', 'call5')
        self.assertEqual(len(e.results), 1)
        self.assertFalse('passed' in e.results.values())
        self.assertTrue('dual-marker' in e.results.values())
        
        self.events.removeEvent('e4', True)
        self.events.removeEvent('e5', True)
