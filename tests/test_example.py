# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from datetime import datetime

from django.test import TestCase
from louis.backends.xml import Backend
from louis.mapper import CollectionMapper, Mapper
from .example_data import payload
from django.db import models


class Event(models.Model):
    external_id = models.IntegerField()
    title = models.CharField(max_length=1024)


class Place(models.Model):
    external_id = models.IntegerField()
    title = models.CharField(max_length=1024)


class Session(models.Model):
    event = models.ForeignKey(Event, related_name="sessions")
    place = models.ForeignKey(Place, related_name="sessions")
    at = models.DateTimeField()


class SessionMapper(CollectionMapper):
    source = 'schedule/session'
    model = Session

    def at(self):
        date_parts = self.data.get('@date').data.split('-')
        time_parts = self.data.get('@time').data.split(':')
        return datetime(*map(int, date_parts + time_parts))

    class place(Mapper):
        source = lambda s: '~places/place[@id={}]'.format(s.data.get('@place').data)
        external_id_field = "external_id"
        model = Place
        external_id = "@id"
        title = "title/text()"

    class event(Mapper):
        source = lambda s: '~events/event[@id={}]'.format(s.data.get('@event').data)
        external_id_field = "external_id"
        model = Event
        external_id = "@id"
        title = "title/text()"


class ManyToOneTest(TestCase):
    def test_saves_as_desired(self):
        backend_data = Backend.parse(payload.encode('utf8'))
        SessionMapper(backend_data).process()
        self.assertEqual(Event.objects.get(external_id=94176).title, "Народный артист. К 90-летию Кирилла Лаврова")
        self.assertEqual(Event.objects.get(external_id=94176).sessions.first().place.title, "Музей-квартира Самойловых")
