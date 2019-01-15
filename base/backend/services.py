# -*- coding: utf-8 -*-
"""
data access layer for our models in the base module
"""
from base.backend.service_base import ServiceBase
from base.models import State


class StateService(ServiceBase):
	"""
	CRUD operations for the State model
	All database transactions involving State model will have to use this class
	"""
	manager = State.objects
