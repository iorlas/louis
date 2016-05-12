# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.utils.functional import cached_property
from django.db.models import ManyToOneRel, ManyToManyRel, ForeignKey


class Mapper(object):
    model = None
    source = None
    external_id_field = None
    many = False

    def __init__(self, data, **kwargs):
        self.data = data

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.context = getattr(self, 'context', {})

        if self.source:
            self.data = self.data.get(self.source, many=self.many)

    @cached_property
    def instance(self):
        external_id = self.get_external_id()
        instance = None
        if external_id is not None:
            instance = self.context.get(self.model, {}).get(external_id)
            if not instance:
                instance = self.model.objects.filter(**{self.external_id_field: external_id}).first()
        instance = instance or self.model()

        if external_id:
            self.context.setdefault(self.model, {})[external_id] = instance
        return instance

    def get_external_id(self):
        if not getattr(self, 'external_id_field', None):
            return None
        if not getattr(self, 'validated_data', None):
            self.gather_data(fields=[self.external_id_field])[self.external_id_field]
        return self.validated_data.get(self.external_id_field)

    def process(self, **additional_data):
        if not self.instance.pk:
            for field, value in additional_data.iteritems():
                setattr(self.instance, field, value)

            for field, value in self.gather_data().iteritems():
                # skip relations, which should be saved after instance save
                if isinstance(value, Mapper):
                    continue
                setattr(self.instance, field, value)
            self.instance.save()

            # relations, which could be save after instance save
            for field, value in self.gather_data().iteritems():
                # filter only post-instance-save relations
                if not isinstance(value, Mapper):
                    continue
                reverse_field_name = self.model._meta.get_field(field).field.name
                value.process(**{
                    reverse_field_name: self.instance
                })
        return self.instance

    def gather_data(self, fields=None):
        self.validated_data = getattr(self, 'validated_data', {})
        fields = fields or (
            field
            for field in dir(self.__class__)
            if field not in dir(Mapper)  # exclude common stuff
        )
        for field in fields:
            value = getattr(self.__class__, field)

            # process relations
            if isinstance(value, type) and issubclass(value, Mapper):
                self.validated_data[field] = value(self.data, parent=self, context=self.context)

                model_field = self.model._meta.get_field(field)
                if isinstance(model_field, (ManyToOneRel, ManyToManyRel)):
                    pass
                elif isinstance(model_field, ForeignKey):
                    self.validated_data[field] = self.validated_data[field].process()

            # process model fields
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

    def process(self, **kwargs):
        if self.many:
            return [
                self.__class__(row, many=False, source=None, **self.kwargs).process(**kwargs)
                for row in self.data
            ]
        return super(CollectionMapper, self).process(**kwargs)

    def get_external_id(self):
        if self.many:
            return [
                self.__class__(row, many=False, source=None, **self.kwargs).get_external_id()
                for row in self.data
            ]
        return super(CollectionMapper, self).get_external_id()

    def gather_data(self, *args, **kwargs):
        if self.many:
            return [
                self.__class__(row, many=False, source=None, **self.kwargs).gather_data(*args, **kwargs)
                for row in self.data
            ]
        return super(CollectionMapper, self).gather_data(*args, **kwargs)