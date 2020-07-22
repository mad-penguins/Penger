import requests

class Penger(object):
	"""docstring for Penger"""
	def __init__(self, token):
		super(Penger, self).__init__()
		self.token = token

	def test(self):
		return True

	def makeRequest(self, method, parameters):
		response = requests.post('https://api.telegram.org/bot' + self.token+ '/' + method, data=parameters)
		json_response = response.json()

		if json_response['ok']:
			return True

	def sendMessage(self, chat_id, text, disable_notification=False, parse_mode=False):
		d = {'chat_id':chat_id, 'text':text, 'disable_notification':disable_notification}

		return self.makeRequest('sendMessage', d)
		