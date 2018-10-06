#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os

def read(path):
	ret = None

	try:
		with open(path) as f:
			ret = f.read()
	except Exception as e:
		pass

	return ret

def write(path, str):
	ret = False

	try:
		with open(path, 'w') as f:
			f.write(str)
		ret = True
	except Exception as e:
		pass

	return ret
