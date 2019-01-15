# -*- coding: utf-8 -*-
"""
tests for the base module model classes
"""
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestModels(object):
	"""
	Tests for the models defined under models.py file
	"""
	def test_state(self):
		"""
		Test for the State model.
		"""
		state = mixer.blend(
			'base.State', name = 'Active', description = 'Items bearing this state will be clear to perform transactions')
		assert state is not None, 'Should create a new State object'
