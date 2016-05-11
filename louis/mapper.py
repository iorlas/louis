# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division


class Mapper(object):
    source = None
    external_id_field = None
    many = False

    def __init__(self, data, **kwargs):
        self.data = data

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        if self.source:
            self.data = self.data.get(self.source, many=self.many)

    def gather_external_id(self):
        if getattr(self, 'external_id_field', None):
            return self.gather_data(fields=[self.external_id_field])[self.external_id_field]

    def process(self):
        external_id = self.get_external_id()
        self.instance = None
        if external_id is not None:
            self.instance = self.Meta.model.objects.filter(**{
                self.Meta.external_id_field: external_id
            }).first()
        if not self.instance:
            self.instance = self.Meta.model(self.gather_data())
        self.save()

    def gather_data(self, fields=None):
        self.validated_data = {}
        fields = fields or (
            field
            for field in dir(self.__class__)
            if not field in dir(Mapper)  # exclude common stuff
        )
        for field in fields:
            value = getattr(self.__class__, field)

            if isinstance(value, Mapper):
                self.validated_data[field] = value(self.data, parent=self).process()
            else:
                query, processor = value if isinstance(value, tuple) else (value, None)
                if callable(query):
                    query = query()
                new_value = self.data.get(query).data
                self.validated_data[field] = processor(new_value) if processor else new_value
        return self.validated_data


class CollectionMapper(Mapper):
    many = True

    def __init__(self, data, **kwargs):
        self.kwargs = kwargs
        super(CollectionMapper, self).__init__(data, **kwargs)

    def process(self):
        if self.many:
            return [
                self.__class__(row, many=False, source=None, **self.kwargs).process()
                for row in self.data
            ]
        return super(CollectionMapper, self).process()

    def gather_external_id(self):
        if self.many:
            return [
                self.__class__(row, many=False, source=None, **self.kwargs).gather_external_id()
                for row in self.data
            ]
        return super(CollectionMapper, self).gather_external_id()

    def gather_data(self, *args, **kwargs):
        if self.many:
            return [
                self.__class__(row, many=False, source=None, **self.kwargs).gather_data(*args, **kwargs)
                for row in self.data
            ]
        return super(CollectionMapper, self).gather_data(*args, **kwargs)