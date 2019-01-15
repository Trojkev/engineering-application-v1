# -*- coding: utf-8 -*-
"""
defines the interfaces that the user will call
"""
import logging

from django.db import transaction
from django.db.models import Q, F, Value
from django.db.models.functions import Concat

from base.backend.services import StateService
from core.backend.services import RiskTypeService, RiskFieldService, CustomerService

lgr = logging.getLogger(__name__)


class Interface(object):
	"""
	class containing the methods that will retrieve, add and manipulate data in the system
	"""
	@staticmethod
	def response(message, status = 'failed', data = None):
		"""
		Returns a standard response to the user after processing the request made
		:param message: the message returned after processing
		:type message: str
		:param status: the status of the transaction
		:type status: str
		:param data: data returned after processing
		:type data: any | None
		:return: a dictionary containing the status, message and data after processing
		:rtype: dict
		"""
		return {'status': status.lower(), 'message': message, 'data': data}

	# @staticmethod
	def get_risk_type(self, risk_type_id):
		"""
		retrieves the RiskType object matching the provided id and it's declared fields
		:param risk_type_id: the unique identifier for the RiskType we are interested in or RiskType Name
		:type risk_type_id: str
		:return: response containing a status, message and data returned after processing
		:rtype: dict
		"""
		try:
			# first we need to ensure risk_type_id is provided, it's expensive to call the db without the id
			if not risk_type_id:
				return self.response('RiskType must be selected')

			# now that we have the id, lets call the risk_type matching that id,
			# note that the user might pass the name instead of the id, so we have to factor that in
			# lastly, we have to use filter instead of get since we might have different RiskTypes
			#  bearing the same name and we need the most recent. get() throws an exception if it encounters more than one result
			risk_type = RiskTypeService().filter(Q(id = risk_type_id) | Q(name = risk_type_id)).order_by(
				'-date_created').first()
			if not risk_type:
				return self.response('selected RiskType does not exist')

			# now we need to retrieve the fields declared for this RiskType
			risk_fields = list(RiskFieldService().filter(
				risk_type = risk_type, state__name = 'Active').order_by('order').values(
				'caption', 'field_type', 'order', 'min_length', 'max_length', 'decimal_places', 'nullable',
				'default_value', 'id'))
			if risk_fields is None:
				return self.response('RiskFields encountered an exception while retrieving values')

			# now that we have both the RiskType and the fields, lets return the data to the user to render the form
			data = {
				'risk_type': {'name': risk_type.name, 'id': risk_type.id},
				'risk_fields': risk_fields
			}
			return self.response('RiskType retrieved successfully', 'success', data)
		except Exception as e:
			lgr.exception('get_risk_type exception: %s', e)
		return self.response('get_risk_type Exception')

	def risk_types(self, request):
		"""
		Retrieves all the RiskTypes defined in the system
		@param request: The Django WSGIRequest to process.
		@type request: WSGIRequest
		@return: response containing a status, message and data returned after processing
		@rtype: dict
		"""
		try:
			# retrieve all the RiskType objects in the system whose state is not Deleted
			# to maintain the db integrity, we shall be marking a record as Deleted once the user 'Deletes' it
			risk_types = list(RiskTypeService().filter(~Q(state__name = 'Deleted')).order_by(
				'-date_created').values(
				'name', 'description', 'state__name', 'id', 'has_form', 'date_created'))
			return self.response('RiskTypes retrieved successfully', 'success', risk_types)
		except Exception as e:
			lgr.exception('risk_types exception: %s', e)
		return self.response('Failed to retrieve the RiskTypes')

	def get_customers(self, request):
		"""
		Retrieves all the RiskTypes defined in the system
		@param request: The Django WSGIRequest to process.
		@type request: WSGIRequest
		@return: response containing a status, message and data returned after processing
		@rtype: dict
		"""
		try:
			# retrieve all the RiskType objects in the system whose state is not Deleted
			# to maintain the db integrity, we shall be marking a record as Deleted once the user 'Deletes' it
			risk_types = list(CustomerService(
				name = Concat(F('first_name'), Value(' '), F('last_name'))).filter(
				~Q(state__name = 'Deleted')).order_by('-date_created').values(
				'name', 'phone_number', 'gender', 'date_of_birth', 'state__name', 'id',
				'email', 'date_created'))
			return self.response('RiskTypes retrieved successfully', 'success', risk_types)
		except Exception as e:
			lgr.exception('risk_types exception: %s', e)
		return self.response('Failed to retrieve the RiskTypes')

	def add_risk_type(self, name, description = None):
		"""
		Creates a new instance of a RiskTye using the provided parameters
		:param name: the name of the RiskType we are creating
		:type name: str
		:param description: description of the the RiskType being created
		:type description: str | None
		:return: dictionary containing processing response
		:rtype: dict
		"""
		try:
			# validate that the name is provided
			if not name:
				return self.response('A required parameter is missing')

			active = StateService().get(name = 'Active')
			# check if there is another Active RiskType with the provided name to avoid duplicates
			risk_type = RiskTypeService().filter(name = name).order_by('-date_created').first()

			# if there exists a RiskType with the provided name, update its status and description if the status is
			# not Active, else return since it already exists and it's Active
			if risk_type is not None:
				if risk_type.state.name != 'Active':
					update = RiskTypeService().update(risk_type.id, description = description, state = active)
					if not update:
						return self.response('Failed to update the RiskType')
					return self.response('Existing RiskType updated successfully', 'success')
				update = RiskTypeService().update(risk_type.id, description = description)
				if not update:
					return self.response('Failed to update the RiskType')
				return self.response('Existing RiskType updated successfully', 'success')

			# now that we are certain the RiskType does not exist, let's create a new one
			risk_type = RiskTypeService().create(name = name, description = description, state = active)
			if not risk_type:
				return self.response('Failed to create a RiskType')
			return self.response('RiskType created successfully', 'success')
		except Exception as e:
			lgr.exception('add_risk_type exception: %s', e)
		return self.response('add_risk_type Exception')

	def add_risk_type_fields(self, risk_type_id, fields):
		"""
		Persists RiskTypeFields selected by the user into the database
		:param risk_type_id: unique identifier for the RiskType we are adding fields for
		:type risk_type_id: str
		:param fields: the fields selected by the user to be added for the specified RiskType
		:type fields: list
		:return: dictionary containing processing response
		:rtype: dict
		"""
		try:
			# ensure required parameters are provided
			if not (risk_type_id or fields):
				return self.response('Some required fields are missing.')

			# check whether the provided RiskType exists, and if it does, check whether it already has a Form
			risk_type = RiskTypeService().get(~Q(state__name = 'Deleted'), id = risk_type_id)
			if not risk_type:
				return self.response('Selected Risk Type does not exist')
			if risk_type.has_form:
				return self.response('The selected RiskType has a Form associated with it already')
			# now lets add the fields for the RiskType and mark it as has_form
			with transaction.atomic():
				try:
					active = StateService().get(name = 'Active')
					for order, s_field in enumerate(fields):
						risk_field = RiskFieldService().create(
							risk_type = risk_type, field_type = s_field.get('field_type'),
							caption = s_field.get('caption'), state = active,
							default_value = s_field.get('default_value'),
							order = order)
						if not risk_field:
							raise Exception('Error creating RiskField')
					risk_type = RiskTypeService().update(risk_type.id, has_form = True)
					if not risk_type:
						raise Exception('RiskType update failed')
				except Exception as e1:
					lgr.exception('add_risk_type_fields atomic exception: %s', e1)
					return self.response('Failed to add fields for the selected RiskType')
			return self.response('RiskType fields added successfully', 'success')
		except Exception as e:
			lgr.exception('add_risk_type_fields exception: %s', e)
		return self.response('Exception creating RiskType fields')

	def register_customer(
			self, first_name, last_name, phone_number, date_of_birth, gender, salutation, email):
		"""
		Registering a new Customer into the system with the provided parameters
		:param first_name: the customer's first name
		:type first_name: str
		:param last_name: the customer's last name
		:type last_name: str
		:param phone_number: the customer's phone number. will be used as the identifier
		:type phone_number: str
		:param date_of_birth: the customer's date of birth
		:type date_of_birth: str
		:param gender: the customer's gender
		:type gender: str
		:param salutation: the customer's social/professional title
		:type salutation: str
		:param email: the customer's email address
		:type email: str
		:return: dictionary containing a response
		:rtype: dict
		"""
		try:
			# lets validate that all the required data is provided
			if not(first_name and last_name and phone_number and date_of_birth and gender and salutation and email):
				return self.response('Some required parameters are missing')
			# now let's check if there exists a Customer with the provided phone number, if so, no need for duplicates
			customer = CustomerService().get(phone_number = phone_number)
			if customer is not None:
				return self.response('Provided phone number is already taken')
			# now we can go ahead and register a Customer with the data
			customer = CustomerService().create(
				first_name = first_name, last_name = last_name,
				phone_number = phone_number, date_of_birth = date_of_birth,
				gender = gender, salutation = salutation,
				email = email, state = StateService().get(name = 'Active'))
			if not customer:
				return self.response('Failed to register customer')
			return self.response('Customer registration successful', 'success')
		except Exception as e:
			lgr.exception('register_customer exception: %s', e)
		return self.response('Exception registering the customer')
