import json
import collections
import decimal
from geopy.distance import vincenty
import pandas as pd
from calendar import timegm


def import_json_file(source):
	"""
	Imports a JSON file as a list of dicts
	"""
	with open(source, 'r') as source:
		reads = list()
		for read in source:
			data = json.loads(read)
			reads.append(data) 
	print "Imported %d reads" % len(reads)
	return reads


def km_between(p1, p2, rounding=3):
	"""Returns distance in km between two geopy points half_even rounded"""
	return half_even(vincenty(p1, p2).km, n_places=rounding) 


def mins_between(from_dt, to_dt):
	"""
	Computes the minutes between from and to datetime objects
	Returns None if either is undefined
	"""
	if from_dt and to_dt:
		return (to_dt - from_dt).total_seconds() / 60.0
	else:
		return None


def geopy_from_geojson(geojson_point):
	"""Extracts geopy-compatible coordinates from a GeoJSON geometry object"""
	lat = half_even(geojson_point['geometry']['coordinates'][1])
	lng = half_even(geojson_point['geometry']['coordinates'][0])
	return (lat, lng)


def half_even(num_val, n_places=4):
	"""
	ROUND_HALF_EVEN a point to n_places decimal places
	"""
	if not 0 < n_places <= 8:
		print "Can only round to 1-8 decimal places. Rounding to default"
		n_places = 4

	try:
		rounding = str(10**int(-1 * n_places))
		x = float(decimal.Decimal("%s" % num_val).quantize(decimal.Decimal(rounding), 
			rounding=decimal.ROUND_HALF_EVEN))
	except ValueError as e:
		e = "Could not round %r" % num_val
		print e
		raise
	return x


def pd_to_unix(panda_ts):
	"""
	Converts pandas timestamp to unix time. This is useful for doing stats on time
	"""
	return timegm(panda_ts.to_datetime().utctimetuple())


def flatten(d, parent_key='', sep='.'):
	"""
	See https://github.com/JimHaughwout/super_flat
	"""
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, collections.MutableMapping):
			items.extend(flatten(v, new_key, sep=sep).items())
		elif isinstance(v, list):
			for elem in v:
				if isinstance(elem, (collections.MutableMapping, list)):
					items.extend(flatten(elem, new_key, sep=sep).items())
				else:
					list_key = new_key + sep + str(v.index(elem))
					items.append((list_key, elem))
		else:
			items.append((new_key, v))
	return dict(items)