# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models


class BaseModel(models.Model):
	"""
	This class abstracts the fields that will be repeated in all models.
	The subsequent models will inherit from this
	"""
	id = models.CharField(max_length = 100, default = uuid.uuid4, unique = True, primary_key = True, editable = False)
	date_modified = models.DateTimeField(auto_now = True, editable = False)
	date_created = models.DateTimeField(auto_now_add = True, editable = True)

	class Meta(object):
		abstract = True


class GenericBaseModel(BaseModel):
	"""
	defines some fields repeated in some models
	"""
	name = models.CharField(max_length = 100)
	description = models.TextField(max_length = 300, null = True, blank = True)

	class Meta(object):
		abstract = True


class State(GenericBaseModel):
	"""
	This class defines the various states in the system. e.g. Active, Deleted
	"""
	def __str__(self):
		return self.name
