# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.db import models


class SimpleModel(models.Model):
    external_id = models.CharField(max_length=1024)
    a = models.CharField(max_length=1024)
