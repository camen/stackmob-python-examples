# Run this after a deployment to verify the following:
#   
#   1) Servers all return the same build tag
#   2) If API, verify GET request returns OK
#
# Author: taylor

import oauth.oauth as oauth
import httplib
import json
import sys

class Client:
	def __init__(self, server, port, key, secret):
		self.server = server
		self.port = port
		self.key = key
		self.secret = secret
  		self.connection = httplib.HTTPConnection(server, port)
		self.consumer = oauth.OAuthConsumer(key, secret)
		
	def _request(self, method, url_path, request_body = False):
		request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_method=method, http_url="http://%s:%d%s" % (self.server, self.port, url_path))
		request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), self.consumer, None)
		headers = request.to_header()
		if(request_body):
			self.connection.request(request.http_method, url, headers=headers, body=request_body)
		else:
			self.connection.request(request.http_method, url, headers=headers)
		return self.connection.getresponse()

	def get(self, path):
		self._request("GET", path)
	def post(self, path, body):
		self._request("POST", path, body)
	def put(self, path, body):
		self._request("PUT", path, body)
	def delete(self, path):
		self._request("DELETE", path)