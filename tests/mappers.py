# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from louis.mapper import Mapper, CollectionMapper
from tests.models import SimpleModel, SimpleNestedModel


class SimpleMapper(Mapper):
    source = 'item'

    external_id = '@id'
    a = '@a'


class SimpleProcessorMapper(Mapper):
    source = 'item'

    external_id = '@id', int
    a = '@a', lambda v: v.split()


class SimpleManyMapper(CollectionMapper):
    source = 'item'

    external_id = '@id', int
    a = '@a'


class SimpleMapperWithExternalID(Mapper):
    source = 'item'
    external_id_field = 'external_id'

    external_id = '@id', int
    a = '@a'


class SimpleManyMapperWithExternalID(CollectionMapper):
    source = 'item'
    external_id_field = 'external_id'

    external_id = '@id', int
    a = '@a'


class SimpleModelMapper(Mapper):
    model = SimpleModel
    external_id_field = 'external_id'

    external_id = '@id', int
    a = '@a'


class SimpleModelWOExternalIDMapper(Mapper):
    model = SimpleModel
    a = '@a'


class SimpleModelManyMapper(CollectionMapper):
    source = 'item'
    model = SimpleModel
    external_id_field = 'external_id'

    external_id = '@id', int
    a = '@a'


class SimpleModelWithNestedMapper(Mapper):
    model = SimpleModel
    external_id_field = 'external_id'

    external_id = '@id', int
    a = '@a'

    class nested(CollectionMapper):
        source = 'nested'
        model = SimpleNestedModel

        b = '@b'


class InvertedNestedMapper(Mapper):
    model = SimpleNestedModel
    b = '@b'

    class simple(Mapper):
        source = 'item'
        model = SimpleModel
        external_id_field = 'external_id'

        external_id = '@id', int
        a = '@a'


class InvertedNestedManyMapper(CollectionMapper):
    source = 'nested'
    model = SimpleNestedModel
    b = '@b'

    class simple(Mapper):
        source = 'item'
        model = SimpleModel
        external_id_field = 'external_id'

        external_id = '@id', int
        a = '@a'