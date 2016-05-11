# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

DEBUG = True

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}