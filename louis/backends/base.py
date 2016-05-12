# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division


class Backend(object):
    """Monad pattern in order to keep common interface for nested parse"""
    @classmethod
    def parse(cls, raw_data):
        raise NotImplementedError()

    def __init__(self, data, root=None):
        self.data = data
        self.root = root or self

    def get(self, query, many=False):
        raise NotImplementedError()
