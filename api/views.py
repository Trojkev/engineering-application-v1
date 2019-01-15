# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
import logging

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.backend.interfaces import Interface

lgr = logging.getLogger(__name__)


class RiskTypes(APIView):
	@method_decorator(csrf_exempt)
	def get(self, request):
		"""
		Api endpoint for the risk_types.
		it will receive a request, forward it to the respective interface and return the result
		:param request: request passed by the user for processing
		:type request: WSGIRequest
		:return: JSonResponse containing processing results
		:rtype: JsonResponse
		"""
		try:
			return JsonResponse(Interface().risk_types(request))
		except Exception as e:
			lgr.exception('risk_types endpoint exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})


class GetAllCustomers(APIView):
	@csrf_exempt
	def get(self, request):
		"""
		Api endpoint for fetching all customers.
		it will receive a request, forward it to the respective interface and return the result
		:param request: request passed by the user for processing
		:type request: WSGIRequest
		:return: JSonResponse containing processing results
		:rtype: JsonResponse
		"""
		try:
			return JsonResponse(Interface().get_customers(request))
		except Exception as e:
			lgr.exception('customers endpoint exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})


class GetRiskType(APIView):
	@csrf_exempt
	def post(self, request):
		"""
		Api endpoint for the risk_types.
		it will receive a request, forward it to the respective interface and return the result
		:param request: request passed by the user for processing
		:type request: WSGIRequest
		:return: JSonResponse containing processing results
		:rtype: JsonResponse
		"""
		try:
			data = json.loads(json.dumps(request.data))
			return JsonResponse(Interface().get_risk_type(risk_type_id = data.get('id')))
		except Exception as e:
			lgr.exception('get_risk_type endpoint exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})


class AddRiskType(APIView):
	@csrf_exempt
	def post(self, request):
		"""
		Api endpoint for creating a RiskType.
		it will receive a request, forward it to the respective interface and return the result
		:param request: request passed by the user for processing
		:type request: WSGIRequest
		:return: JSonResponse containing processing results
		:rtype: JsonResponse
		"""
		try:
			data = json.loads(json.dumps(request.data))
			return JsonResponse(Interface().add_risk_type(data.get('name'), data.get('description')))
		except Exception as e:
			lgr.exception('add_risk_type endpoint exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})


class AddRiskTypeFields(APIView):
	@csrf_exempt
	def post(self, request):
		"""
		Api endpoint for creating RiskFields and mapping them to a RiskType.
		it will receive a request, forward it to the respective interface and return the result
		:param request: request passed by the user for processing
		:type request: WSGIRequest
		:return: JSonResponse containing processing results
		:rtype: JsonResponse
		"""
		try:
			data = json.loads(json.dumps(request.data))
			return JsonResponse(Interface().add_risk_type_fields(data.get('id'), data.get('fields')))
		except Exception as e:
			lgr.exception('add_risk_type_fields endpoint exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})


class RegisterCustomer(APIView):
	@csrf_exempt
	def post(self, request):
		"""
		Api endpoint for registering a new Customer into the system.
		it will receive a request, forward it to the respective interface and return the result
		:param request: request passed by the user for processing
		:type request: WSGIRequest
		:return: JSonResponse containing processing results
		:rtype: JsonResponse
		"""
		try:
			data = json.loads(json.dumps(request.data))
			return JsonResponse(Interface().register_customer(
				data.get('first_name'), data.get('last_name'), data.get('phone_number'), data.get('date_of_birth'),
				data.get('gender'), data.get('salutation'), data.get('email')))
		except Exception as e:
			lgr.exception('add_risk_type_fields endpoint exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})
