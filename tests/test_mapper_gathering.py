# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.xml import Backend
from .mappers import SimpleMapper, SimpleProcessorMapper, SimpleManyMapper, SimpleMapperWithExternalID, SimpleManyMapperWithExternalID


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

    def test_many_gathering(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <item id="1" a="x" />
                <item id="2" a="b" />
            </feed>
        '''.encode())

        mapper = SimpleManyMapper(backend_data)
        data = mapper.gather_data()
        self.assertEqual(data[0]['external_id'], 1)
        self.assertEqual(data[0]['a'], 'x')
        self.assertEqual(data[1]['external_id'], 2)
        self.assertEqual(data[1]['a'], 'b')


class MapperExternalIDGatheringTest(TestCase):
    def test_returns_none_when_mapper_does_not_support_it(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <item id="1" a="bcd" />
            </feed>
        '''.encode())

        mapper = SimpleMapper(backend_data)
        data = mapper.gather_external_id()
        self.assertEqual(data, None)

    def test_gathers_external_id_only(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <item id="1" a="bcd" />
            </feed>
        '''.encode())

        mapper = SimpleMapperWithExternalID(backend_data)
        data = mapper.gather_external_id()
        self.assertEqual(data, 1)

    def test_many_mode(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <item id="1" />
                <item id="2" />
            </feed>
        '''.encode())

        mapper = SimpleManyMapperWithExternalID(backend_data)
        data = mapper.gather_external_id()
        self.assertEqual(data, [1, 2])