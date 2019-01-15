# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from core.models import Customer, RiskType, RiskField, Risk, RiskData


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	"""
	Admin class for the Customer model. defines which fields to display and which are searchable
	"""
	list_filter = ('date_created',)
	list_display = (
		'salutation', 'first_name', 'last_name', 'gender', 'phone_number', 'date_of_birth', 'email', 'state',
		'date_modified', 'date_created')
	search_fields = (
		'salutation', 'first_name', 'last_name', 'gender', 'phone_number', 'date_of_birth', 'email', 'state__name')


@admin.register(RiskType)
class RiskTypeAdmin(admin.ModelAdmin):
	"""
	Admin class for the RiskType model. defines which fields to display and which are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'has_form', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')


@admin.register(RiskField)
class RiskFieldAdmin(admin.ModelAdmin):
	"""
	Admin class for the RiskField model. defines which fields to display and which are searchable
	"""
	list_filter = ('date_created',)
	list_display = (
		'risk_type', 'field_type', 'caption', 'min_length', 'max_length', 'nullable', 'max_digits', 'decimal_places',
		'default_value', 'order', 'state', 'date_modified', 'date_created')
	search_fields = ('risk_type__name', 'field_type', 'caption', 'default_value', 'order')


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
	"""
	Admin class for the Risk model. defines which fields to display and which are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('customer', 'risk_type', 'state', 'date_modified', 'date_created')
	search_fields = (
		'customer__first_name', 'customer__last_name', 'customer__identity_number', 'customer__other_name',
		'risk_type__name', 'state__name')


@admin.register(RiskData)
class RiskDataAdmin(admin.ModelAdmin):
	"""
	Admin class for the RiskData model. defines which fields to display and which are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('risk', 'risk_field', 'value', 'state', 'date_modified', 'date_created')
	search_fields = (
		'risk__customer__first_name', 'risk__customer__last_name', 'risk__customer__identity_number',
		'risk__risk_type__name', 'state__name')
