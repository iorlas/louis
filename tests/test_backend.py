# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.base import Backend


class BackendTest(TestCase):
    def test_keeps_received_data_as_expected(self):
        b = Backend(123)
        self.assertEqual(b.data, 123)
