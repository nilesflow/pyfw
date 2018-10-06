#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import sys
import os
from time import time

def trace():
	"""
	エラー発生個所
	"""
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

	return [exc_type, fname, exc_tb.tb_lineno]

def uniqid(prefix = ''):
	"""
	13桁のuniqidを生成
	http://www.php2python.com/wiki/function.uniqid/
	"""
	return prefix + hex(int(time()))[2:10] + hex(int(time()*1000000) % 0x100000)[2:7]
