# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from base.models import GenericBaseModel, BaseModel, State


def salutation():
	"""
	Returns a collection of salutation titles to choose from
	@return: salutation choices
	@rtype tuple
	"""
	return (
		('Prof', 'Professor'), ('Dr', 'Doctor'),
		('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Miss'))


def gender():
	"""
	Returns a collection of gender to choose from
	@return: gender choices
	@rtype: tuple
	"""
	return (
		('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))


def field_types():
	return (
		('text', 'Text'),
		('number', 'Number'),
		('date', 'Date'),
		('email', 'Email'),
		('file', 'File')
	)


class Customer(BaseModel):
	"""
	When a customer subscribes for a cover, we will store their personal data here.
	"""
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	salutation = models.CharField(max_length = 5, choices = salutation())
	phone_number = models.CharField(max_length = 50, unique = True)
	gender = models.CharField(max_length = 6, choices = gender())
	date_of_birth = models.DateField()
	email = models.CharField(max_length = 50)
	state = models.ForeignKey(State, on_delete = models.CASCADE)

	def __str__(self):
		return '%s %s %s' % (self.salutation, self.first_name, self.last_name)


class RiskType(GenericBaseModel):
	"""
	Defines the RiskTypes that the insurer will support. e.g. Automobile Cover, House Cover etc.
	"""
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	has_form = models.BooleanField(default = False)  # indicates whether there is a form defined for this RiskType

	def __str__(self):
		return self.name


class RiskField(BaseModel):
	"""
	Maps the RiskType defined by the user to the requirements(Fields) selected to store the data.
	The UI form will be rendered using values From this model
	"""
	risk_type = models.ForeignKey(RiskType, on_delete = models.CASCADE)
	field_type = models.CharField(max_length = 30, choices = field_types())
	caption = models.CharField(max_length = 100)  # This is the label that will be used for the widget in the UI form
	min_length = models.IntegerField(default = 0, null = True, blank = True)  # minimum characters the field can store
	max_length = models.IntegerField(default = 255, null = True, blank = True)  # maximum characters the field can store
	nullable = models.BooleanField(default = False)  # whether this field is mandatory
	max_digits = models.IntegerField(default = 20, null = True, blank = True)  # in case this is a DecimalField
	decimal_places = models.IntegerField(default = 2, null = True, blank = True)  # in case this is a DecimalField
	default_value = models.CharField(max_length = 100, null = True, blank = True)  # placeholder if no value provided
	order = models.IntegerField(default = 1, null = True, blank = True)  # the position which the widget will be on UI
	state = models.ForeignKey(State, on_delete = models.CASCADE)

	def __str__(self):
		return '%s %s %s' % (self.risk_type.name, self.field_type, self.caption)


class Risk(BaseModel):
	"""
	maps the Customers to the RiskType they have subscribed to. e.g: AutoMobile Cover - Kevin Macharia
	"""
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE)  # the customer who has subscribed for a cover
	risk_type = models.ForeignKey(RiskType, on_delete = models.CASCADE)  # the RiskType they have subscribed to
	state = models.ForeignKey(State, on_delete = models.CASCADE)

	def __str__(self):
		return '%s - %s %s' % (self.risk_type.name, self.customer.first_name, self.customer.last_name)


class RiskData(BaseModel):
	"""
	Maps the fields selected by the insurer as required for the risk they are covering to the data provided by the
	customer subscribing to the risk cover. e.g: AutoMobile Cover - Kevin Macharia - Registration Number : KZB 302Y
	"""
	risk = models.ForeignKey(Risk, on_delete = models.CASCADE)
	risk_field = models.ForeignKey(RiskField, on_delete = models.CASCADE)
	value = models.CharField(max_length = 255)
	state = models.ForeignKey(State, on_delete = models.CASCADE)

	def __str__(self):
		return '%s - %s %s - %s : %s' % (
			self.risk.risk_type.name, self.risk.customer.first_name, self.risk.customer.last_name,
			self.risk_field.caption, self.value)
