#!/usr/bin/env python
'''
	Author			: Chaitanya Kumar Guduru
	Organization	: Teradata
	Tool			: Version Check Tool
	Module_Name		: File loader and writer
'''

import json

def loader(file, log):
	log('\nOpening file '+file, 2)
	with open(file+'.json', 'r') as f:
		data = json.load(f)
	f.close()
	log('\n-'+ file +' file read, creating datastructure.\n', 2)
	return data

def exporter(data, file):
	f = open(file, 'w')
	f.write(data)
	f.close()