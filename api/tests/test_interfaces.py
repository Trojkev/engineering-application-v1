# -*- coding: utf-8 -*-
"""
test for the interfaces
"""
import pytest
from mixer.backend.django import mixer

from api.backend.interfaces import Interface

pytestmark = pytest.mark.django_db


class TestInterfaces(object):
	"""
	Tests for the interface methods
	"""
	def test_get_risk_type(self):
		"""
		Test for the get_risk_type() API interface
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		mixer.cycle(5).blend(
			'core.RiskField', risk_type = risk_type, min_length = 5, max_length = 80, state = state)

		response = Interface().get_risk_type(risk_type_id = risk_type.id)
		assert response['status'] == 'success', 'Should successfully return a RiskType with its associated Fields'

		# should also pass when we provide Name instead of id
		response = Interface().get_risk_type(risk_type_id = 'AutoMobile Cover')
		assert response['status'] == 'success', 'Should successfully return a RiskType with its associated Fields'

	def test_risk_types(self):
		"""
		Test for the risk_types API interface
		"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.cycle(5).blend('core.RiskType', state = state)
		response = Interface().risk_types({})
		assert response['status'] == 'success', 'Should successfully return the RiskTypes retrieved'

	def test_add_risk_type(self):
		"""
		Test for the add_risk_type API interface
		"""
		state = mixer.blend('base.State', name = 'Active')
		response = Interface().add_risk_type('', 'some description here')
		assert response['message'] == 'A required parameter is missing'

		response = Interface().add_risk_type('Robbery Cover', 'Covers homes and property against robbery')
		assert response['message'] == 'RiskType created successfully'

		# this should update an existing RiskType instead of creating a new one.
		mixer.blend('core.RiskType', name = 'Robbery Cover', state = state)
		response = Interface().add_risk_type('Robbery Cover', 'Covers homes and property against robbery')
		assert response['message'] == 'Existing RiskType updated successfully'

	def test_add_risk_type_fields(self):
		"""
		Test for the add_risk_type_fields API interface
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'Automobile Cover', state = state)
		fields = [
			{'caption': 'First Name', 'field_type': 'text'},
			{'caption': 'Date of Birth', 'field_type': 'date'}]
		response = Interface().add_risk_type_fields(risk_type.id, fields)
		assert response['status'] == 'success', 'Should return success upon processing'

	def test_register_customer(self):
		"""
		Test for the register_customer API interface
		"""
		mixer.blend('base.State', name = 'Active')
		response = Interface().register_customer('', 'Macharia', '', '', 'Male', 'Mr', '')
		assert response['message'] == 'Some required parameters are missing'

		response = Interface().register_customer(
			first_name = 'Kevin', last_name = 'Macharia', phone_number = '254717072416', date_of_birth = '1993-04-08',
			gender = 'Male', salutation = 'Mr', email = 'kelvinmacharia078@gmail.com')
		assert response['status'] == 'success', 'Should successfully create a new Customer'
