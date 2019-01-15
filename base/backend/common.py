# coding=utf-8
"""
The common utilities used across the system.
This defines the methods and functions that perform common functionality required to get thingy's done.
"""
import base64
import binascii
import json
import os
import logging
import hashlib
from datetime import datetime, timedelta, date
from decimal import Decimal

from django.http import QueryDict, JsonResponse
from django.db.models import Q

from pytz import timezone

lgr = logging.getLogger(__name__)


def hash_pin(text):
	"""
	Encrypts a text using hashlib library with sha512
	@param text: the text that is being encrypted
	@return: encrypted text
	"""
	hashed_str = None
	try:
		plain_text = str(text)
		m = hashlib.sha1()
		m.update(plain_text)
		x = m.hexdigest()
		n = hashlib.sha512()
		n.update(x)
		hashed_str = n.hexdigest()
	except Exception as e:
		lgr.error('hash_pin error:%s' % e)
	return hashed_str


def entity_timezone_aware(time_stamp, entity_timezone):
	"""
	Convert datetime to owner timezone
	@param time_stamp: The timestamp we are converting to timezone aware.
	@type time_stamp: datetime
	@param entity_timezone: The timezone for the entity to make aware.
	@type entity_timezone: str
	@return: The passed in timestamp converted to the respective timezone of the entity.
	@rtype: datetime
	"""
	try:
		return time_stamp.astimezone(timezone(entity_timezone))
	except Exception as e:
		lgr.exception('corporate_timezone_aware Exception: %s', e)
	return time_stamp


def generate_token():
	"""
	Generates a standard token to be used for ABC + etc.
	@return:
	"""
	try:
		return base64.b64encode(binascii.hexlify(os.urandom(15)).decode())
	except Exception as e:
		lgr.exception('generate_token Exception: %s', e)
	return None


def generate_table_response(data = None, draw = 1, records_filtered = 0, records_total = 0, error = None):
	"""
	This function generates the table response for data table consumers.
	@param data: The data from the queryset.
	@type data: list | None
	@param draw: The data-table draw param as sent form client side.
	@type draw: int
	@param records_filtered: The total records count filtered from the queryset.
	@type records_filtered: int
	@param records_total: The total records in the queryset.
	@type records_total: int
	@param error: The error string, if any.
	@type error: str | None
	@return: A JSON response with the data-table request packaged accordingly.
	@rtype: JsonResponse
	"""
	try:
		if draw is None:
			draw = []
		return JsonResponse({
			'draw': draw, 'data': data, 'error': error, 'recordsFiltered': records_filtered,
			'recordsTotal': records_total
		})
	except Exception as e:
		lgr.exception('Exception: %s', e)
	return JsonResponse({'draw': 0, 'data': [], 'error': 'Server error.', 'recordsFiltered': 0, 'recordsTotal': 0})


def get_error_table_response(draw = 0, error = 'Error occurred retrieving data'):
	"""
	Retrieves the default DT responses in case of an error.
	@param draw: The DT draw request.
	@type draw: int
	@param error: An error message to be returned to DT.
	@type error: str
	@return: The DT dict that should be encoded accordingly.
	@rtype: dict
	"""
	return {'draw': draw, 'data': [], 'error': error, 'recordsFiltered': 0, 'recordsTotal': 0}


def pop_first_none_empty_from_list(list_items):
	"""
	Gets the fist item in the list that's not empty then removes that item from the list.
	Awesome.
	@param list_items: The items to check.
	@type list_items: list
	@return: The item that's not empty and the list with the item removed.
	@rtype: tuple
	"""
	try:
		length = len(list_items)
		local_list = list_items
		for _ in range(0, length):
			field = local_list.pop(0)  # Always pop the first item as other items might have already been removed.
			if len(str(field)) > 0:
				return field, local_list
	except Exception as e:
		lgr.exception('pop_first_none_empty_from_list Exception: %s', e)
	return '', list_items


def build_search_query(search_value, columns, extra_columns = None):
	"""
	Builds a search query using Q objects, ORed together.
	@param search_value: The value to search for.
	@param columns: Columns to carry out searching in.
	@type columns: list
	@param extra_columns: A list of Extra columns that we don't want to include on the main columns.
	@type extra_columns: list | None
	@return: Q objects
	@rtype: Q
	"""
	try:
		if isinstance(extra_columns, list):
			columns += extra_columns
		if len(str(search_value)) > 0:
			if len(columns) > 0:
				field, fields = pop_first_none_empty_from_list(columns)
				query = Q(('%s__icontains' % str(field), str(search_value)))
				for fl in fields:
					if fl != '' and str(search_value) != '':
						query |= Q(('%s__icontains' % fl, str(search_value)))
				return query
	except Exception as e:
		lgr.exception('build_search_query Exception: %s', e)
	return ~Q(date_created = None)


def extract_ordering(order, columns = list(), default_sort = '-date_created'):
	"""
	Extracts the ordering from a DT request
	@param order: The DT request order field. Comes in structure [{column:0, dir: 'asc'}]
	@param columns: The columns definition according to the database models. If none is provided,
	we assume the order came with valid DB columns.
	@param default_sort: The default sorting criteria if an exception occurs. String.
	@return: A tuple with the columns sorted validly.
	@rtype: tuple
	"""
	try:
		ordering = list()
		order = list(order)
		for ord_item in order:
			ord_item = dict(ord_item)
			column = int(ord_item.get('column', 0))
			sort = str(ord_item.get('dir', 'asc'))
			# Valid sorting direction
			if sort == 'asc':
				sort = ''
			else:
				sort = '-'
			if len(columns) > column:
				if columns[column] is not None and len(str(columns[column])) > 3:
					ordering.append(str(sort + str(columns[column])))
			elif len(str(ord_item.get('column', 0))) > 3:  # Assume a named column at least 3 chars
				ordering.append(str(sort + str(ord_item.get('column', ''))))
		if len(ordering) > 0:
			return tuple(ordering)
		return default_sort,
	except Exception as e:
		lgr.exception('extract_ordering Exception: %s', e)
	return default_sort,


def extract_dt_columns(dt_columns):
	"""
	Extracts the DT columns from the request sent by DataTables.
	@param dt_columns: The list of DT columns.
	@type dt_columns: list[dict]
	@return: Returns a list of the columns by DT.
	@rtype: list
	"""
	clean_cols = map(lambda x: x.get('data', ''), dt_columns)
	if 'id' not in clean_cols:
		clean_cols += ['id']
	return clean_cols


def extract_not_none(columns):
	"""
	Extracts the items in the list that are not None and returns the list.
	@param columns: The list of items to
	@type columns: list
	@return: Returns the list but with the empty or None items removed.
	@rtype: list
	"""
	new_list = []
	for col in columns:
		if col is not None and len(col) > 0:
			new_list.append(col)
	return new_list


def get_request_data(request):
	"""
	Retrieves the request data irrespective of the method and type it was send.
	@param request: The Django HttpRequest.
	@type request: WSGIRequest
	@return: The data from the request as a dict
	@rtype: QueryDict
	"""
	try:
		data = None
		if request is not None:
			request_meta = getattr(request, 'META', {})
			request_method = getattr(request, 'method', None)
			if request_meta.get('CONTENT_TYPE', '') == 'application/json':
				data = json.loads(request.body)
			elif str(request_meta.get('CONTENT_TYPE', '')).startswith('multipart/form-data;'):  # Special handling for
				# Form Data?
				data = request.POST.copy()
				data = data.dict()
			elif request_method == 'GET':
				data = request.GET.copy()
				data = data.dict()
			elif request_method == 'POST':
				data = request.POST.copy()
				data = data.dict()
			if not data:
				request_body = getattr(request, 'body', None)
				if request_body:
					data = json.loads(request_body)
				else:
					data = QueryDict()
			return data
	except Exception as e:
		lgr.exception('get_request_data Exception: %s', e)
	return QueryDict()


def json_super_serializer(obj):
	"""
	Automatic serializer for objects not serializable by default by the JSON serializer.
	Includes datetime, date, Decimal
	@param obj: The object to convert.
	@return: String of the data converted.
	@rtype: str
	"""
	if isinstance(obj, datetime):
		# noinspection PyBroadException
		try:
			return obj.strftime('%d/%m/%Y %I:%M:%S %p')
		except Exception:
			return str(obj)
	elif isinstance(obj, date):
		# noinspection PyBroadException
		try:
			return obj.strftime('%d/%m/%Y')
		except Exception:
			return str(obj)
	elif isinstance(obj, (Decimal, float)):
		return str("{:,}".format(round(Decimal(obj), 2)))
	elif isinstance(obj, timedelta):
		return obj.days
	return str(obj)
