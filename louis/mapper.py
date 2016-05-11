# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division


class Mapper(object):
    class Meta:
        source = None
        many = True
        external_id_field = 'external_id'

    @property
    def is_many_mode(self):
        return getattr(self.Meta, 'many', True) and not self.is_many_instance

    def __init__(self, data, parent=None, is_many_instance=False):
        self.data = data
        self.is_many_instance = is_many_instance
        if getattr(self.Meta, 'source', None) and not self.is_many_instance:
            self.data = self.data.get(self.Meta.source, many=getattr(self.Meta, 'many', True))

    def process(self):
        if self.is_many_mode:
            return [self.__class__(row, is_many_instance=True).process() for row in self.data]
        return self._process_item()

    def gather_external_id(self):
        if self.is_many_mode:
            return [self.__class__(row, is_many_instance=True).gather_external_id() for row in self.data]
        if hasattr(self.Meta, 'external_id_field'):
            return self.gather_data(fields=[self.Meta.external_id_field])[self.Meta.external_id_field]

    def _process_item(self, data):
        external_id = self.get_external_id()
        if self.get_external_id() is not None:
            self.instance = self.Meta.model.objects.filter(**{
                self.Meta.external_id_field: external_id
            }).first()
        if not self.instance:
            self.instance = self.Meta.model(self.gather_data())
        self.save()

    def gather_data(self, fields=None):
        if self.is_many_mode:
            return [self.__class__(row, is_many_instance=True).gather_data(fields=fields) for row in self.data]

        validated_data = {}
        fields = fields or (
            field
            for field in self.__class__.__dict__
            if not field.startswith('__') and not field[0].isupper()
        )
        for field in fields:
            value = self.__class__.__dict__[field]

            if isinstance(value, Mapper):
                pass
            else:
                query, processor = value if isinstance(value, tuple) else (value, None)
                if callable(query):
                    query = query()
                new_value = self.data.get(query).data
                validated_data[field] = processor(new_value) if processor else new_value

        return validated_data
