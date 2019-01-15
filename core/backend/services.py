# -*- coding: utf-8 -*-
"""
data access layer for our models in the base module
"""
from base.backend.service_base import ServiceBase
from core.models import Customer, Risk, RiskData, RiskField, RiskType


class CustomerService(ServiceBase):
	"""
	CRUD operations for the Customer model
	All database transactions involving Customer model will have to use this class
	"""
	manager = Customer.objects


class RiskService(ServiceBase):
	"""
	CRUD operations for the Risk model
	All database transactions involving Risk model will have to use this class
	"""
	manager = Risk.objects


class RiskDataService(ServiceBase):
	"""
	CRUD operations for the RiskData model
	All database transactions involving RiskData model will have to use this class
	"""
	manager = RiskData.objects


class RiskFieldService(ServiceBase):
	"""
	CRUD operations for the RiskField model
	All database transactions involving RiskField model will have to use this class
	"""
	manager = RiskField.objects


class RiskTypeService(ServiceBase):
	"""
	CRUD operations for the RiskType model
	All database transactions involving RiskType model will have to use this class
	"""
	manager = RiskType.objects
