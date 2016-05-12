# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.xml import Backend
from .mappers import SimpleModelWithNestedMapper, InvertedNestedMapper, InvertedNestedManyMapper
from .models import SimpleModel


class ManyToOneTest(TestCase):
    def test_saves_as_desired(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="1" a="bcd">
                <nested b="http://ya.ru/1.jpg"/>
            </item>
        '''.encode())

        mapper = SimpleModelWithNestedMapper(backend_data)
        with self.assertNumQueries(3):
            mapper.process()
        self.assertEqual(SimpleModel.objects.get(external_id=1).a, "bcd")
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.count(), 1)
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.first().b, "http://ya.ru/1.jpg")

    def test_multiple(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="8" a="bcd">
                <nested b="http://ya.ru/1.jpg"/>
                <nested b="http://ya.ru/2.jpg"/>
                <nested b="http://ya.ru/65.jpg"/>
            </item>
        '''.encode())

        mapper = SimpleModelWithNestedMapper(backend_data)
        with self.assertNumQueries(5):
            mapper.process()
        self.assertEqual(SimpleModel.objects.get(external_id=8).a, "bcd")
        self.assertEqual(SimpleModel.objects.get(external_id=8).nested.count(), 3)
        self.assertEqual(SimpleModel.objects.get(external_id=8).nested.all()[0].b, "http://ya.ru/1.jpg")
        self.assertEqual(SimpleModel.objects.get(external_id=8).nested.all()[1].b, "http://ya.ru/2.jpg")
        self.assertEqual(SimpleModel.objects.get(external_id=8).nested.all()[2].b, "http://ya.ru/65.jpg")


class ForeignKeyTest(TestCase):
    def test_saves_nested_as_desired(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <nested b="http://ya.ru/1.jpg">
                <item id="1" a="bcd" />
            </nested>
        '''.encode())

        mapper = InvertedNestedMapper(backend_data)
        with self.assertNumQueries(3):
            mapper.process()
        self.assertEqual(SimpleModel.objects.get(external_id=1).a, "bcd")
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.count(), 1)
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.first().b, "http://ya.ru/1.jpg")

    def test_multiple(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <feed>
                <nested b="http://ya.ru/1.jpg">
                    <item id="1" a="bcd" />
                </nested>
                <nested b="http://ya.ru/65.jpg">
                    <item id="1" a="bcd" />
                </nested>
            </feed>
        '''.encode())

        mapper = InvertedNestedManyMapper(backend_data)
        with self.assertNumQueries(5):
            mapper.process()
        self.assertEqual(SimpleModel.objects.get(external_id=1).a, "bcd")
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.count(), 2)
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.all()[0].b, "http://ya.ru/1.jpg")
        self.assertEqual(SimpleModel.objects.get(external_id=1).nested.all()[1].b, "http://ya.ru/65.jpg")