# -*- coding: utf-8 -*-
"""
tests for the models defined in the core module
"""
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestModels(object):
	"""
	Tests for the core Models
	"""
	def test_customer(self):
		"""
		Test for the Customer model
		"""
		state = mixer.blend('base.State', name = 'Active')
		customer = mixer.blend(
			'core.Customer', first_name = 'Kevin', last_name = 'Macharia', phone_number = '11111122222',
			salutation = 'Mr', gender = 'M', state = state)
		assert customer is not None, 'Should create a Customer object'

	def test_risk_type(self):
		"""
		Test for the RiskType model
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		assert risk_type is not None, 'Should return a RiskType object'

	def test_risk_field(self):
		"""
		Test for the RiskField model
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		risk_field = mixer.blend(
			'core.RiskField', risk_type = risk_type, field_type = 'text', caption = 'Registration Number', order = 3,
			max_length = 30, state = state)
		assert risk_field is not None, 'Should return an instance of a RiskField'

	def test_risk(self):
		"""
		Test for the Risk model
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		customer = mixer.blend('core.Customer', first_name = 'Kevin', last_name = 'Macharia', state = state)
		risk = mixer.blend('core.Risk', customer = customer, risk_type = risk_type, state = state)
		assert risk is not None, 'Should return a Risk object'

	def test_risk_data(self):
		"""
		Test for the RiskData model
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		customer = mixer.blend('core.Customer', first_name = 'Kevin', last_name = 'Macharia', state = state)
		risk_field = mixer.blend(
			'core.RiskField', risk_type = risk_type, field_type = 'text', caption = 'Registration Number', order = 3,
			max_length = 30, state = state)
		risk = mixer.blend('core.Risk', customer = customer, risk_type = risk_type, state = state)
		risk_data = mixer.blend(
			'core.RiskData', risk = risk, risk_field = risk_field, value = 'KZQ 001A', state = state)
		assert risk_data is not None, 'Should return a RiskData object'
