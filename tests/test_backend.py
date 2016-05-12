# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.test import TestCase
from louis.backends.base import Backend


class BackendTest(TestCase):
    def test_keeps_received_data_as_expected(self):
        b = Backend(123)
        self.assertEqual(b.data, 123)

    def test_keeps_root_element_as_self_by_default(self):
        b = Backend(123)
        self.assertIs(b.root, b)

    def test_keeps_given_root_element(self):
        b = Backend(123, 1)
        self.assertIs(b.root, 1)