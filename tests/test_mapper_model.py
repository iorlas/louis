# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.xml import Backend
from .mappers import SimpleModelMapper
from .models import SimpleModel


class MapperModelInstanceTest(TestCase):
    def test_will_search_for_model_in_context_first(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="1" a="bcd" />
        '''.encode())

        instance = SimpleModel(external_id=1)
        mapper = SimpleModelMapper(backend_data, context={
            SimpleModel: {
                1: instance
            }
        })
        with self.assertNumQueries(0):
            self.assertIs(mapper.instance, instance)

    def test_will_search_in_db_by_external_id(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="3" a="bcd" />
        '''.encode())

        SimpleModel.objects.create(external_id=5)
        SimpleModel.objects.create(external_id=534)
        SimpleModel.objects.create(external_id=169)
        instance = SimpleModel.objects.create(external_id=3)
        mapper = SimpleModelMapper(backend_data)
        with self.assertNumQueries(1):
            self.assertEqual(mapper.instance.id, instance.id)

    def test_will_create_new_instance_when_nothing_is_found(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="3" a="bcd" />
        '''.encode())

        mapper = SimpleModelMapper(backend_data)
        with self.assertNumQueries(1):
            self.assertEqual(mapper.instance.id, None)
            self.assertIsInstance(mapper.instance, SimpleModel)

    def test_populates_context_with_instance(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="3" a="bcd" />
        '''.encode())

        context = {}
        mapper = SimpleModelMapper(backend_data, context=context)
        mapper.instance
        self.assertIsInstance(context[SimpleModel][3], SimpleModel)


class MapperModelInstanceSaveTest(TestCase):
    def test_saves_new_instance_in_db(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="1" a="bcd" />
        '''.encode())

        mapper = SimpleModelMapper(backend_data)
        with self.assertNumQueries(2):
            mapper.process()

        instance = SimpleModel.objects.get(external_id=1)
        self.assertEqual(instance.a, "bcd")

    def test_will_not_save_again_existing_object(self):
        backend_data = Backend.parse('''<?xml version="1.0" encoding="utf8"?>
            <item id="1" a="bcd" />
        '''.encode())

        instance = SimpleModel.objects.create(external_id=1)
        mapper = SimpleModelMapper(backend_data)
        with self.assertNumQueries(1):
            mapper.process()
