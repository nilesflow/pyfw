#!/usr/bin/env python
# -*- coding: utf-8 -*-

# user modules
from pyfw.error.error import Error

class RecognitionError(Error):
	"""
	例外クラス：テキスト変換失敗エラー
	"""

	def __init__(self, description):
		super(RecognitionError, self).__init__("recognition_error", description)
