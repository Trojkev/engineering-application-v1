# -*- coding: utf-8 -*-
"""
Decorators used in the API
"""
import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import available_attrs
from django.utils.six import wraps

lgr = logging.getLogger(__name__)


def enable_spa(fn):
	"""Ensures JSON response"""

	def json_wrap(*args, **kwargs):
		"""Wrap with JSON"""
		req = 0
		for k in args:
			if isinstance(k, WSGIRequest):
				if k.method == 'OPTIONS':
					response = JsonResponse({'status': 'success'})
					response['Allow'] = 'get,post,options'
					response['Access-Control-Allow-Origin'] = '*'
					response['Access-Control-Allow-Credentials'] = True
					response['Access-Control-Allow-Headers'] = 'Content-Type,Pragma,Cache-Control'
					response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
					return response
				response = fn(*args, **kwargs)
				response['Allow'] = 'get,post,options'
				response['Access-Control-Allow-Origin'] = '*'
				response['Access-Control-Allow-Credentials'] = True
				response['Access-Control-Allow-Headers'] = 'Content-Type,Pragma,Cache-Control'
				response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
				return response
			req += 1

	return wraps(fn, assigned = available_attrs(fn))(json_wrap)
