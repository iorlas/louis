# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import importlib
from .backends.xml import Backend as DefaultBackend


class Source(object):
    backend = 'xml'

    def __init__(self):
        if isinstance(self.backend, [basestring]):
            module = importlib.import_module('louis.backends.{}'.format(self.backend))
            self.backend = module.Backend

    def __call__(self, raw_data):
        backend = self.backend(raw_data)
