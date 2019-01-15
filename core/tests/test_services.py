# -*- coding: utf-8 -*-
"""
Tests for the model services in the base module
"""
import pytest
from mixer.backend.django import mixer

from core.backend.services import CustomerService, RiskFieldService, RiskService, RiskDataService, RiskTypeService

pytestmark = pytest.mark.django_db


class TestCustomerService(object):
	"""
	Test for the CustomerService class
	"""
	def test_get(self):
		"""
		Test for the CustomerService get(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		obj = mixer.blend('core.Customer', first_name = 'Kevin', last_name = 'Macharia', state = state)
		customer = CustomerService().get(id = obj.id, first_name = 'Kevin')
		assert customer is not None, 'Should return a Customer instance with first_name Kevin'

		customer = CustomerService().get(state__name = 'Inactive')
		assert customer is None, 'Should return None since there is no customer with state Inactive'

	def test_filter(self):
		"""
		Test for the CustomerService filter(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.cycle(5).blend('core.Customer', first_name = 'Kevin', state = state)

		customers = CustomerService().filter(state__name = 'Active')
		assert len(customers) == 5, 'Should return 5 Customer objects with state Active'

		customers = CustomerService().filter(state__name = 'Inactive')
		assert len(customers) == 0, 'Should return an empty queryset as there are no Customers with state Inactive'

	def test_create(self):
		"""
		Test for the CustomerService create(**kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		customer = CustomerService().create(
			first_name = 'Kevin',
			last_name = 'Macharia',
			salutation = 'Mr',
			phone_number = '111222333',
			date_of_birth = '1993-04-08',
			email = 'kelvinmacharia078@gmail.com',
			state = state
		)
		assert customer is not None, 'Should create a Customer instance with the passed parameters'

		customer = CustomerService().create(
			first_name = '',
			last_name = 'Macharia',
			salutation = 'Mr',
			phone_number = '',
			date_of_birth = '08-04-1993',
			email = '',
			state = state
		)
		assert customer is None, 'Should fail because some of the required fields are not provided'

	def test_update(self):
		"""
		Test for the CustomerService update(pk, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		obj = mixer.blend('core.Customer', last_name = 'Macharia', state = state)
		customer = CustomerService().update(obj.id, first_name = 'Kevin')
		assert customer is not None, 'Should update a Customer instance with first_name Kevin'

		customer = CustomerService().update(obj, first_name = 'Kevin')
		assert customer is None, 'Should fail since obj is not a valid uuid for the Customer object'


class TestRiskTypeService(object):
	"""
	Test for the RiskTypeService
	"""
	def test_get(self):
		"""
		Test for the RiskTypeService get(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		obj = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_type = RiskTypeService().get(id = obj.id, name = 'AutoMobile Cover')
		assert risk_type is not None, 'Should return a RiskType with name AutoMobile Cover'

		risk_type = RiskTypeService().get(state__name = 'Deleted')
		assert risk_type is None, 'Should fail because there is no RiskType with state Deleted'

	def test_filter(self):
		"""
		Test for the RiskTypeService filter(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.cycle(4).blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_types = RiskTypeService().filter(state__name = 'Active')
		assert len(risk_types) == 4, 'Should return 4 instances of RiskType with state Active'

		risk_types = RiskTypeService().filter(state__name = 'Deleted')
		assert len(risk_types) == 0, 'Should return an empty queryset because there is no RiskTypes with state Deleted'

	def test_create(self):
		"""
		Test for the RiskTypeService create(**kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = RiskTypeService().create(
			name = 'AutoMobile Cover',
			description = 'All vehicles will be insured through this product',
			state = state
		)
		assert risk_type is not None, 'Should create a RiskType object'

		risk_type = RiskTypeService().create(
			name = None,
			description = 'All vehicles will be insured through this product',
			state = state
		)
		assert risk_type is None, 'Should fail because name is required and nothing was passed'

	def test_update(self):
		"""
		Test for the RiskTypeService update(pk, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		obj = mixer.blend('core.RiskType', name = 'House Cover', state = state)
		risk_type = RiskTypeService().update(obj.id, name = 'AutoMobile Cover')
		assert risk_type is not None, 'Should update the RiskType with name AutoMobile Cover'

		risk_type = RiskTypeService().update(obj, name = 'Deleted')
		assert risk_type is None, 'Should fail because obj is not a valid uuid'


class TestRiskFieldService(object):
	"""
	Test for the RiskFieldService
	"""
	def test_get(self):
		"""
		Test for the RiskFieldService get(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		obj = mixer.blend(
			'core.RiskField', field_type = 'text', risk_type = risk_type, state = state, caption = 'Registration Number')
		risk_field = RiskFieldService().get(id = obj.id)
		assert risk_field is not None, 'Should Return a RiskField object'

		risk_field = RiskFieldService().get(state__name = 'Approval Pending')
		assert risk_field is None, 'Should fail because there is no RiskField with state Approval Pending'

	def test_filter(self):
		"""
		Test for the RiskFieldService filter(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.cycle(5).blend('core.RiskField', state = state)
		risk_fields = RiskFieldService().filter(state__name = 'Active')
		assert len(risk_fields) == 5, 'Should return 5 RiskFields with state Active'

		risk_fields = RiskFieldService().filter(state__name = 'Approval Pending')
		assert len(risk_fields) == 0, 'Should return an empty queryset'

	def test_create(self):
		"""
		Test for the RiskFieldService create(**kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_field = RiskFieldService().create(
			field_type = 'text',
			risk_type = risk_type,
			caption = 'Registration Number',
			min_length = 2,
			max_length = 50,
			order = 2,
			state = state
		)
		assert risk_field is not None, 'Should create a RiskField object with the provided parameters'

		risk_field = RiskFieldService().create(
			field_type = 'text',
			risk_type = risk_type,
			caption = 'Registration Number',
			min_length = 2,
			max_length = 50,
			order = 2,
			state = state
		)
		assert risk_field is None, 'Should return None because field attribute should be of type Field'

	def test_update(self):
		"""
		Test for the RiskFieldService update(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		obj = mixer.blend(
			'core.RiskField', field_type = 'text', risk_type = risk_type, caption = 'Registration Number')
		risk_field = RiskFieldService().update(obj.id, state = state)
		assert risk_field is not None, 'Should update a RiskField object with a new state'

		risk_field = RiskFieldService().update(obj, state = state)
		assert risk_field is None, 'Should fail because obj is not a valid uuid'


class TestRiskService(object):
	"""
	Test for the RiskService
	"""
	def test_get(self):
		"""
		Test for the RiskService get(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		customer = mixer.blend('core.Customer', first_name = 'Kevin', state = state)
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		obj = mixer.blend('core.Risk', risk_type = risk_type, customer = customer, state = state)

		risk = RiskService().get(id = obj.id)
		assert risk is not None, 'Should return a Risk object matching the provided id'

		risk = RiskService().get(customer__last_name = 'Macharia')
		assert risk is None, 'Should return None since there is no risk whose customer last_name is Macharia'

	def test_filter(self):
		"""
		Test for the RiskService filter(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		customer = mixer.blend('core.Customer', first_name = 'Kevin', state = state)
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		mixer.cycle(5).blend('core.Risk', risk_type = risk_type, customer = customer, state = state)

		risks = RiskService().filter(state__name = 'Active')
		assert len(risks) == 5, 'Should return 5 instances of Risk with state Active'

		risks = RiskService().filter(state__name = 'Pending Approval')
		assert len(risks) == 0, 'Should return an empty queryset'

	def test_create(self):
		"""
		Test for the RiskService create(**kwargs)
		"""
		state = mixer.blend('base.State', name = 'Active')
		customer = mixer.blend('core.Customer', first_name = 'Kevin', state = state)
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk = RiskService().create(
			customer = customer,
			risk_type = risk_type,
			state = state
		)
		assert risk is not None, 'Should create a Risk object with the provided parameters'

		risk = RiskService().create(
			customer = risk_type,
			risk_type = customer,
			state = state
		)
		assert risk is None, 'Should return None because some required parameters do not match the ones provided'

	def test_update(self):
		"""
		Test for the RiskService update(pk, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		customer = mixer.blend('core.Customer', first_name = 'Kevin', state = state)
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		obj = mixer.blend('core.Risk', risk_type = risk_type, customer = customer)

		risk = RiskService().update(obj.id, state = state)
		assert risk is not None, 'Should update a Risk object with the provided state'

		risk = RiskService().update(obj, state = state)
		assert risk is None, 'Should return None since the the pk provided is invalid'


class TestRiskDataService(object):
	"""
	Test for the RiskDataService
	"""
	def test_get(self):
		"""
		Test for the RiskDataService get(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_field = mixer.blend(
			'core.RiskField', risk_type = risk_type, field_type = 'text', caption = 'Registration Number', state = state)
		risk = mixer.blend('core.Risk', state = state)
		obj = mixer.blend('core.RiskData', risk_field = risk_field, risk = risk, value = 'KZQ 001Y')

		risk_data = RiskDataService().get(id = obj.id, value = 'KZQ 001Y')
		assert risk_data is not None, 'Should return a RiskData object with value KZQ 001Y'

		risk_data = RiskDataService().get(value = 'KZQ001Y')
		assert risk_data is None, 'Should return None since there is no RiskData with value KZQ001Y'

	def test_filter(self):
		"""
		Test for the RiskDataService filter(*args, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_field = mixer.blend(
			'core.RiskField', risk_type = risk_type, field_type = 'text', caption = 'Registration Number', state = state)
		risk = mixer.blend('core.Risk', state = state)
		mixer.cycle(5).blend('core.RiskData', risk_field = risk_field, risk = risk, value = 'KZQ 001Y')

		risk_data = RiskDataService().filter(value = 'KZQ 001Y')
		assert len(risk_data) == 5, 'Should return 5 RiskData objects with value KZQ 001Y'

		risk_data = RiskDataService().filter(value = 'KZQ001Y')
		assert len(risk_data) == 0, 'Should return an empty queryset'

	def test_create(self):
		"""
		Test for the RiskDataService create(**kwargs)
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_field = mixer.blend(
			'core.RiskField', risk_type = risk_type, field_type = 'text', caption = 'Registration Number', state = state)
		risk = mixer.blend('core.Risk', state = state)
		risk_data = RiskDataService().create(
			risk_field = risk_field,
			risk = risk,
			value = 'KZQ 001Y',
			state = state
		)
		assert risk_data is not None, 'Should create a RiskData object with the provided parameters'

		risk_data = RiskDataService().create(
			risk_field = risk,
			risk = risk_field,
			value = 'KZQ 001Y',
			state = state
		)
		assert risk_data is None, 'Should return None since provided parameters do not match the expected ones'

	def test_update(self):
		"""
		Test for the RiskDataService update(pk, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_field = mixer.blend(
			'core.RiskField', risk_type = risk_type, field_type = 'text', caption = 'Registration Number', state = state)
		risk = mixer.blend('core.Risk', state = state)
		obj = mixer.blend('core.RiskData', risk_field = risk_field, risk = risk, value = 'KZQ')

		risk_data = RiskDataService().update(obj.id, value = 'KZQ 001Y')
		assert risk_data is not None, 'Should update a RiskData object with value KZQ 001Y'

		risk_data = RiskDataService().update(obj, value = 'KZQ001Y')
		assert risk_data is None, 'Should return None since provided pk is invalid'
