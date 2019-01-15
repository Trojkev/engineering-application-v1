# -*- coding: utf-8 -*-
"""
Tests for the model services in the base module
"""
import pytest
from mixer.backend.django import mixer

from base.backend.services import StateService

pytestmark = pytest.mark.django_db


class TestStateService(object):
	"""
	Test for the StateService
	"""
	def test_get(self):
		"""
		Test for the StateService get(*args, **kwargs) method
		"""
		mixer.blend('base.State', name = 'Active')
		obj = StateService().get(name = 'Active')
		assert obj is not None, 'Should return a State instance with name ACTIVE'

	def test_filter(self):
		"""
		Test for the StateService filter(*args, **kwargs) method
		"""
		mixer.cycle(3).blend('base.State', name = 'Active')
		obj = StateService().filter(name = 'Active')
		assert len(obj) == 3, 'Should return 3 State instances with name ACTIVE'

	def test_create(self):
		"""
		Test for the StateService create(**kwargs) method
		"""
		obj = StateService().create(
			name = 'Active', description = 'initializes all the ACTIVE state')
		assert obj is not None, 'Should create a new State with name ACTIVE'

	def test_update(self):
		"""
		Test for the StateService update(pk, **kwargs) method
		"""
		state = mixer.blend('base.State', name = 'Active')
		new_state = StateService().update(state.id, name = 'In Transit')
		assert new_state is not None, 'Should update the State object with a new name'
