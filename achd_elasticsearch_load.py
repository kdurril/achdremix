#!/usr/bin/python3
#
#Basic ElasticSearch loader

from json import loads
from pyelasticsearch import bulk, index_op


with open('json/achd_match.json', 'r') as f:
	inspections = loads(f.read())

bulk((index_op(doc, id=doc.pop('inspect_id')) for doc in inspections),\
	index='achd', doc_type='record')

