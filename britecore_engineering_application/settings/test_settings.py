# -*- coding: utf-8 -*-
"""
defines the test settings and db
"""
from britecore_engineering_application.settings.base import *


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
	}
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
