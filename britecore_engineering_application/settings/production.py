# -*- coding: utf-8 -*-
"""
production settings for this project
"""
from .base import *

import dj_database_url

ENVIRONMENT = 'production'
DEBUG = config('DEBUG', default=False)
ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'))
