import requests

class Penger(object):
	"""docstring for Penger"""
	def __init__(self, token):
		super(Penger, self).__init__()
		self.token = token
		self.apiAddress = "https://api.telegram.org/"
		self.response = None

	def getToken(self):
		return self.token

	def setToken(self, token):
		self.token = token

	def getAPIaddress(self):
		return self.apiAddress

	def getResponse(self):
		return self.response

	def setResponse(self, response):
		self.response = response

	def test(self):
		return True

	def isSuccessfulRequest(self):
		return self.response.json()['ok']

	def makeRequest(self, method, parameters):
		self.response = requests.post(self.apiAddress + 'bot' + self.token+ '/' + method, data=parameters)

		return self.isSuccessfulRequest()

	def sendMessage(self, chat_id, text, disable_notification=False, parse_mode=False):
		parameters = {'chat_id':chat_id, 'text':text, 'disable_notification':disable_notification}

		return self.makeRequest('sendMessage', parameters)
		