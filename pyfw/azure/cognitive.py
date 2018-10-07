#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os
import time
import json
import requests

# user modules
from pyfw.libs import file
from pyfw.http import Http
from pyfw.error.error import InternalError
from pyfw.azure.error import RecognitionError

class Cognitive:
	"""
	音声サービスのREST API
	https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/rest-apis
	"""

	def __init__(self, **kargs):
		self.logger = kargs['logging'].getLogger(__name__)
		self.key = kargs['key']

		# トークン管理
		self.path_token = kargs['path_temp'] + '/token_cognitive'

	def _refleshToken(self):
		"""
		クラス内のアクセストークンを更新
		"""

		# ファイル存在チェック
		path = self.path_token;
		token = None
		if not os.path.exists(path):
			# 無ければ新規作成
			pass
		else:
			# 有れば有効切れチェック（10分なので9分）
			# https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/rest-apis

			target = os.stat(path).st_mtime
			now = time.time()
			self.logger.info(target)
			self.logger.info(now)
			if now - 9 * 60 > target:
				# 期限切れなら再作成
				pass
			else:
				# 期限内なら、ファイルから読みこむ
				token = file.read(path) # 失敗時、None

		# 再作成
		if token is None:
			token = self.issueToken()
			file.write(path, token)

		# クラス内に保持
		self.token = token

	def issueToken(self):
		"""
		アクセストークンの取得
		"""

		res = requests.post(
			url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken",
			headers = {
				"Content-type": "application/x-www-form-urlencoded",
				"Content-Length": "0",
				"Ocp-Apim-Subscription-Key": self.key,
			}
		)
		self.logger.info(res)

		if res.status_code != requests.codes.ok:
			raise InternalError("faild to convert text.")

		res.encoding = "utf-8"
		self.logger.info(res.text)
		token = res.text

		return token

	def recognition(self, data,
			params = {'language' : 'ja-JP'},
			format = {'mime': 'audio/wav', 'codec': 'audio/pcm', 'samplerate': '44100'}
		):
		"""
		Speech to Text API
		"""

		# アクセストークンのリフレッシュ
		self._refleshToken()

		# APIでwav -> text変換
		res = requests.post(
			url = "https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1",
			params = params,
			data = data,
			headers = {
				"Content-type": format['mime'] + "; codec=" + format['codec'] + "; samplerate="+ format['samplerate'] + ";",
				"Authorization": self.token
			}
		)
		self.logger.info(res)

		if res.status_code != requests.codes.ok:
			raise InternalError("faild to convert text.")

		# 文字化けするのでutf-8で扱うことを明示する
		res.encoding = "utf-8"
		self.logger.info(res.text)

		try:
			result = json.loads(res.text)
		except Exception as e:
			self.logger.error(e)
			raise InternalError("converted result is invalid json format.")

		# https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech/concepts
		status = result['RecognitionStatus']
		if status in ['InitialSilenceTimeout', 'NoMatch', 'BabbleTimeout']:
			raise RecognitionError("faild to convert text, RecognitionStatus is not error. ")
		elif status != 'Success':
			raise InternalError("faild to convert text, RecognitionStatus is error. ")

		self.logger.info(result)
		text = result['DisplayText']

		return text
