import oauth.oauth as oauth
import httplib
import json
import sys

class BaseClient:
	
	def __init__(self, baseURL, key, secret):
		self.url = baseURL
		self.connection = httplib.HTTPConnection(baseURL)
		self.consumer = oauth.OAuthConsumer(key, secret)
		
	def _execute(self, httpmethod, path, body):
		request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_method=httpmethod, http_url="http://" + self.url + "/" + path)
		request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), self.consumer, None)
		headers = request.to_header()
		headers["Content-Type"] = "application/json"
		headers["Accept"] = "application/vnd.stackmob+json; version=0"
		self.connection.set_debuglevel(1)
		bodyString = ""
		if(body != None):
			bodyString = json.dumps(body)
		self.connection.request(request.http_method, "/"+path, body=bodyString, headers=headers)
		return self.connection.getresponse()

	def get(self, path):
		self._execute("GET", path, None)
	def post(self, path, body):
		self._execute("POST", path, body)
	def put(self, path, body):
		self._execute("PUT", path, body)
	def delete(self, path):
		self._execute("DELETE", path, None)

class APIClient(BaseClient):
	def __init__(self, key, secret):
		super.__init__("api.mob1.stackmob.com", key, secret)

class PushAPIClient(BaseClient):
	def __init__(self, key, secret):
		super.__init__("push.mob1.stackmob.com", key, secret)
