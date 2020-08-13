import requests


class Penger(object):
	"""docstring for Penger"""
	def __init__(self, token=None, updateID=0, senderWhitelist=None,
			chatWhitelist=None, accordance=None, emptyAccordance=None):
		super(Penger, self).__init__()
		self.token = token
		self.apiAddress = "https://api.telegram.org/"
		self.response = None
		self.updateID = updateID
		self.senderWhitelist = senderWhitelist
		self.chatWhitelist = chatWhitelist
		self.accordance = accordance
		self.emptyAccordance = emptyAccordance


	def test(self):
		return True


	def isSuccessfulRequest(self):
		return self.response.json()['ok']


	def makeRequest(self, method, parameters, files=None):
		if files is None:
			self.response = requests.post(self.apiAddress + 'bot' + \
					self.token+ '/' + method, data=parameters)
		else:
			self.response = requests.post(self.apiAddress + 'bot' + \
					self.token+ '/' + method, data=parameters, files=files)
		return self.isSuccessfulRequest()


	def sendMessage(self, chat_id, text, disable_notification=False, parse_mode=False):
		parameters = {'chat_id':chat_id, 'text':text, 'disable_notification':disable_notification}

		return self.makeRequest('sendMessage', parameters)


	def sendImage(self, chat_id, image, text=None, disable_notification=False, parse_mode=False):
		if text is None:
			parameters = {'chat_id':chat_id, 'disable_notification':disable_notification}
		else:
			parameters = {'chat_id':chat_id, 'caption':text, 'disable_notification':disable_notification}

		files = {'photo': image}

		return self.makeRequest('sendPhoto', parameters, files)


	def getDataFromUpdate(self, updateJSON):
		data = {'update_id': updateJSON['update_id']}

		data['sender_id'] = updateJSON['message']['from']['id']

		data['chat_id'] = updateJSON['message']['chat']['id']

		data['text'] = updateJSON['message']['text']

		return data


	def runAccordance(self, data):
		if self.accordance is not None and data['text'] in self.accordance:
			self.accordance[data['text']](data)
		elif self.emptyAccordance is not None:
			self.emptyAccordance(data)


	def respondToMessage(self, updateJSON):
		print(updateJSON)
		data = self.getDataFromUpdate(updateJSON)
		print()
		print(data)

		if self.senderWhitelist is not None and data['sender_id'] in self.senderWhitelist:
			if self.chatWhitelist is not None and data['chat_id'] in self.chatWhitelist:
				self.runAccordance(data)

		return data['update_id']


	def updateAndRespond(self):
		status = self.makeRequest('getUpdates', None)
		updatesJSON = self.response.json()

		for updateJSON in updatesJSON['result']:
			if updateJSON['update_id'] > self.updateID and 'message' in updateJSON:
				self.updateID = self.respondToMessage(updateJSON)


		return status
