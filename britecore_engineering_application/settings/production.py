# -*- coding: utf-8 -*-
"""
production settings for this project
"""
from .base import *

import dj_database_url

ENVIRONMENT = 'production'
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
