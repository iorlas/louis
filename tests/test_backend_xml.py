# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.xml import Backend


class XMLBackendTest(TestCase):
    def test_parses_simple_xml_data(self):
        backend = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed version="1.1">
            </feed>
        '''.encode())
        self.assertIsNotNone(backend.data)

    def test_retrieves_data_and_gives_same_interface(self):
        backend = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed version="1.1">
                <schedule>
                    <session/>
                </schedule>
            </feed>
        '''.encode())

        data = backend.get('schedule/session')
        self.assertIsInstance(data, Backend)

    def test_retrieves_multiple_data_by_query_as_list_with_same_interface(self):
        backend = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed version="1.1">
                <schedule>
                    <session/>
                    <session/>
                    <session/>
                    <session/>
                </schedule>
            </feed>
        '''.encode())

        data = backend.get('schedule/session', many=True)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for i in data:
            self.assertIsInstance(i, Backend)

    def test_retrieves_single_data_by_query_by_default(self):
        backend = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed version="1.1">
                <session var="ololo"/>
            </feed>
        '''.encode())

        data = backend.get('session/@var').data
        self.assertEqual(data, 'ololo')
