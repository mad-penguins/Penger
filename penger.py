import logging
import requests


class Penger(object):
    """docstring for Penger"""

    def __init__(self, token='None', updateID=0, senderWhitelist=None, chatWhitelist=None, accordance=None,
                 emptyAccordance=None, loggingFile='penger.log', loggingFilemode='a', loggingLevel=logging.INFO,
                 loggingFormat='[%(asctime)s]# %(levelname)-8s %(name)s: %(message)s'):

        super(Penger, self).__init__()

        self.token = token
        self.apiAddress = "https://api.telegram.org/"
        self.response = None
        self.updateID = updateID
        self.senderWhitelist = senderWhitelist
        self.chatWhitelist = chatWhitelist
        self.accordance = accordance
        self.emptyAccordance = emptyAccordance

        logging.basicConfig(filename=loggingFile, filemode=loggingFilemode, format=loggingFormat, level=loggingLevel)
        self.logger = logging.getLogger('Penger')

        self.logger.debug('Creating a Penger object.')

    def test(self):
        return True

    def logStatus(self, status, logMessage):
        if status:
            self.logger.info(logMessage + ' STATUS: ' + str(status))
        else:
            self.logger.error(logMessage + ' STATUS: ' + str(status))
        return status

    def isSuccessfulRequest(self):
        return self.response.json()['ok']

    def makeRequest(self, method, parameters, files=None):
        if files is None:
            self.response = requests.post(self.apiAddress + 'bot' + self.token + '/' + method, data=parameters)
        else:
            self.response = requests.post(self.apiAddress + 'bot' + self.token + '/' + method, data=parameters,
                                          files=files)
        return self.isSuccessfulRequest()

    def sendMessage(self, chat_id, text, disable_notification=False, parse_mode=False):
        parameters = {'chat_id': chat_id, 'text': text, 'disable_notification': disable_notification}

        return self.logStatus(self.makeRequest('sendMessage', parameters),
                              f'Sending message. chat_id: {chat_id}, notification: {not disable_notification}.')

    def sendImage(self, chat_id, image, text=None, disable_notification=False, parse_mode=False):
        files = {'photo': image}
        if text is None:
            parameters = {'chat_id': chat_id, 'disable_notification': disable_notification}
        else:
            parameters = {'chat_id': chat_id, 'caption': text, 'disable_notification': disable_notification}

        return self.logStatus(self.makeRequest('sendPhoto', parameters, files),
                              f'Sending image to chat_id: {chat_id}, notification: {not disable_notification}.')

    def getDataFromUpdate(self, updateJSON):
        data = {'update_id': updateJSON['update_id'], 'sender_id': updateJSON['message']['from']['id'],
                'chat_id': updateJSON['message']['chat']['id'], 'text': updateJSON['message']['text']}

        self.logger.debug('Getting data from Update.')

        return data

    def runAccordance(self, data):
        if self.accordance is not None and data['text'] in self.accordance:
            self.accordance[data['text']](data)
        elif self.emptyAccordance is not None:
            self.emptyAccordance(data)

    def respondToMessage(self, updateJSON):
        data = self.getDataFromUpdate(updateJSON)

        if self.senderWhitelist is not None and data['sender_id'] in self.senderWhitelist:
            if self.chatWhitelist is not None and data['chat_id'] in self.chatWhitelist:
                self.runAccordance(data)

    def updateAndRespond(self):
        status = self.logStatus(self.makeRequest('getUpdates', None),
                                'Getting updates.')
        updatesJSON = self.response.json()

        for updateJSON in updatesJSON['result']:
            if updateJSON['update_id'] > self.updateID and 'message' in updateJSON:
                self.logger.info(f'Update: {updateJSON}'.encode('ascii', errors='ignore').decode())
                self.respondToMessage(updateJSON)
            elif updateJSON['update_id'] > self.updateID:
                self.logger.warning(f'Update: {updateJSON}'.encode('ascii', errors='ignore').decode())
            self.updateID = updateJSON['update_id']

        return status
