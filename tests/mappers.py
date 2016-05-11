# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from louis.mapper import Mapper


class SimpleMapper(Mapper):
    class Meta:
        source = 'item'
        many = False

    external_id = '@id'
    a = '@a'


class SimpleProcessorMapper(Mapper):
    class Meta:
        source = 'item'
        many = False

    external_id = '@id', int
    a = '@a', lambda v: v.split()


class SimpleManyMapper(Mapper):
    class Meta:
        source = 'item'
        many = True

    external_id = '@id', int
    a = '@a'


class SimpleMapperWithExternalID(Mapper):
    class Meta:
        source = 'item'
        many = False
        external_id_field = 'external_id'

    external_id = '@id', int
    a = '@a'


class SimpleManyMapperWithExternalID(SimpleMapperWithExternalID):
    class Meta(SimpleMapperWithExternalID.Meta):
        many = True
