# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from base.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	"""
	Admin class for the state model. defines the fields to display and which ore searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)
