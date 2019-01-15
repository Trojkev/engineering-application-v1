# -*- coding: utf-8 -*-
import json
import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer
from api.views import GetRiskType, RiskTypes, AddRiskType

pytestmark = pytest.mark.django_db


class TestApiViews(object):
	"""
	Tests for the ApiViews
	"""
	def test_risk_types(self):
		"""
		Test for the RiskTypes get endpoint
		"""
		state = mixer.blend('base.State', name = 'Active')
		mixer.cycle(5).blend('core.RiskType', state = state)
		request = RequestFactory().get('api/risk_types/')
		response = RiskTypes().get(request)
		assert json.loads(response.content)['status'] == 'success', 'Should successfully return the RiskTypes retrieved'

	def test_get_risk_type(self):
		"""
		Test for the GetRiskType get endpoint
		"""
		state = mixer.blend('base.State', name = 'Active')
		risk_type = mixer.blend('core.RiskType', name = 'AutoMobile Cover', state = state)
		mixer.cycle(5).blend(
			'core.RiskField', risk_type = risk_type, min_length = 5, max_length = 80, state = state)
		request = RequestFactory().post('api/get_risk_type/', {'risk_type_id': risk_type.id})
		response = GetRiskType().post(request)
		assert json.loads(response.content)['status'] == 'success',\
			'Should successfully return a RiskType with its associated Fields'

	def test_add_risk_type(self):
		"""
		Test for the AddRiskType post endpoint
		"""
		mixer.blend('base.State', name = 'Active')
		request = RequestFactory().post(
			'api/add_risk_type/', {'name': 'Robbery Cover', 'description': 'Cover against theft and robbery'})
		response = AddRiskType().post(request)
		# assert json.loads(response.content)['status'] == 'success', 'Should create a RiskType successfully'
