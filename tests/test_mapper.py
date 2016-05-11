# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.xml import Backend
from .mappers import SimpleMapper, SimpleProcessorMapper


class MapperGatheringTest(TestCase):
    def test_gathers_data(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <item id="1" a="bcd" />
            </feed>
        '''.encode())

        mapper = SimpleMapper(backend_data)
        data = mapper.gather_data()
        self.assertEqual(data['external_id'], '1')
        self.assertEqual(data['a'], 'bcd')

    def test_gathers_data_with_processor(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <item id="1" a="a b" />
            </feed>
        '''.encode())

        mapper = SimpleProcessorMapper(backend_data)
        data = mapper.gather_data()
        self.assertEqual(data['external_id'], 1)
        self.assertEqual(data['a'], ['a', 'b'])
