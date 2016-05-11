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
            self.assertIs(mapper.get_model_instance(), instance)
