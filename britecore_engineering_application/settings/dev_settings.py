# -*- coding: utf-8 -*-
"""
development settings for this project
	- should be disabled in production
"""
import dj_database_url

from .base import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
	}
}

DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'))
