# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division


class Mapper(object):
    class Meta:
        source = None
        many = True

    def __init__(self, data, parent=None):
        self.data = data
        if getattr(self.Meta, 'source', None):
            self.data = self.data.get(self.Meta.source)

    def process(self):
        if getattr(self.Meta, 'many', True):
            return map(self._process_item, self.data)
        return self._process_item(self.data)

    def _process_item(self, data):
        mapped_data = {}
        for field, val in self.__class__.__dict__.iteritems():
            if field.startswith('__') or field[0].isupper():
                continue

            if isinstance(val, Mapper):
                pass
            else:
                query, processor = val if isinstance(val, tuple) else (val, None)
                if callable(query):
                    query = query()
                new_value = data.get(query).data
                mapped_data[field] = processor(new_value) if processor else new_value

        # self._save(self, mapped_data)
