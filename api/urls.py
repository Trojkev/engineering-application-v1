# -*- coding: utf-8 -*-

from django.conf.urls import url

from api.views import GetRiskType, RiskTypes, AddRiskType, AddRiskTypeFields, GetAllCustomers, RegisterCustomer

urlpatterns = [
	url(r'risk_types/', RiskTypes().as_view(), name = 'risk_types'),
	url(r'get_risk_type/', GetRiskType().as_view(), name = 'get_risk_type'),
	url(r'add_risk_type/', AddRiskType().as_view(), name = 'add_risk_type'),
	url(r'add_risk_type_fields/', AddRiskTypeFields().as_view(), name = 'add_risk_type_fields'),
	url(r'customers/', GetAllCustomers().as_view(), name = 'customers'),
	url(r'register_customer/', RegisterCustomer().as_view(), name = 'register_customer'),
]
