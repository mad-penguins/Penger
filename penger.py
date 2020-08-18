import time
import logging
import requests


class Penger(object):
    """docstring for Penger"""

    def __init__(self, token='None', updateID=0,
                 mainSender=None, privateSenderList=[], senderWhitelist=[], senderBlacklist=[],
                 mainChat=None, privateChatList=[], chatWhitelist=[], chatBlacklist=[],
                 accordance=[], emptyAccordance=None,
                 loggingFile='penger.log', loggingFilemode='a', loggingLevel=logging.INFO,
                 loggingFormat='[%(asctime)s]# %(levelname)-8s %(name)s: %(message)s'):

        super(Penger, self).__init__()

        self.token = token
        self.apiAddress = "https://api.telegram.org/"

        self.response = None
        self.updateID = updateID

        self.mainSender = mainSender
        self.privateSenderList = privateSenderList
        self.senderWhitelist = senderWhitelist
        self.senderBlacklist = senderBlacklist

        self.mainChat = mainChat
        self.privateChatList = privateChatList
        self.chatWhitelist = chatWhitelist
        self.chatBlacklist = chatBlacklist

        self.accordance = accordance
        self.emptyAccordance = emptyAccordance

        logging.basicConfig(filename=loggingFile, filemode=loggingFilemode, format=loggingFormat, level=loggingLevel)
        self.logger = logging.getLogger('Penger')

        self.logger.debug('Creating a Penger object.')

    def logStatus(self, status, logMessage):
        if status:
            self.logger.info(logMessage + ' STATUS: ' + str(status))
        else:
            self.logger.error(logMessage + ' STATUS: ' + str(status))
        return status

    def test(self):
        return self.logStatus(True, 'This is Penger-test.')

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
        if chat_id == 'mainC':
            chat_id = self.mainChat
        parameters = {'chat_id': chat_id, 'text': text, 'disable_notification': disable_notification}

        return self.logStatus(self.makeRequest('sendMessage', parameters),
                              f'Sending message. chat_id: {chat_id}, notification: {not disable_notification}.')

    def sendMessageToMainChat(self, text, disable_notification=False, parse_mode=False):
        self.sendMessage(self.mainChat, text, disable_notification, parse_mode)

    def sendMessageToChat(self, data, text, disable_notification=False, parse_mode=False):
        self.sendMessage(data['chat_id'], text, disable_notification, parse_mode)

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

        self.logger.debug(f'Getting data from Update: {data}')

        return data

    def startEmptyAccordance(self, data, hash=None):
        if hash is None:
            hash = '{0:010x}'.format(int(time.time() * 256))[4:]

        if self.emptyAccordance is not None:
            if str(type(self.emptyAccordance)) == "<class 'penger.Accordance'>":
                self.logger.info(f'Start of the empty Accordance-{hash}...')
                self.emptyAccordance.checkAndRun(penger=self, data=data)
                self.logger.info(f'End of the empty Accordance-{hash}.')
            else:
                self.logger.info('Start of the empty accordance (base function)...')
                self.emptyAccordance(data)
                self.logger.info('End of the empty accordance (base function).')

    def SearchAccordance(self, data):
        hash = '{0:010x}'.format(int(time.time() * 256))[4:]

        for acc in self.accordance:
            if str(type(acc)) == "<class 'penger.Accordance'>":
                if acc.text == data['text']:
                    self.logger.info(f'Start of the Accordance-{hash}...')
                    acc.checkAndRun(penger=self, data=data)
                    self.logger.info(f'End of the Accordance-{hash}.')
                    return
            else:
                if acc == data['text']:
                    self.logger.info('Start of the accordance (from dict)...')
                    self.accordance[acc](data)
                    self.logger.info('End of the accordance (from dict).')
                    return
        self.startEmptyAccordance(data, hash)

    def respondToMessage(self, updateJSON):
        data = self.getDataFromUpdate(updateJSON)

        if data['sender_id'] not in self.senderBlacklist and data['chat_id'] not in self.chatBlacklist:
            self.logger.debug('Start search accordance.')
            self.SearchAccordance(data)
        else:
            self.logger.warning('Sender and/or Chat blocked.')

    def updateAndRespond(self):
        status = self.logStatus(self.makeRequest('getUpdates', None),
                                'Getting updates.')
        updatesJSON = self.response.json()

        if self.updateID == 0:
            self.updateID = updatesJSON['result'][len(updatesJSON['result'])-1]['update_id']

        for updateJSON in updatesJSON['result']:
            if updateJSON['update_id'] > self.updateID and 'message' in updateJSON:
                self.logger.info(f'Update: {updateJSON}'.encode('ascii', errors='ignore').decode())
                self.respondToMessage(updateJSON)
            elif updateJSON['update_id'] > self.updateID:
                self.logger.warning(f'Update: {updateJSON}'.encode('ascii', errors='ignore').decode())

            if updateJSON['update_id'] > self.updateID:
                self.logger.debug(f'[updateID={self.updateID}] Update...')
                self.updateID = updateJSON['update_id']
                self.logger.debug(f'Updated. [updateID={self.updateID}]')

        return status


class Accordance(object):
    def __init__(self, text, func, quick='all:all', isEnable=True, enableArgument=False, ifNotAuthorized=None,
                 senderWhitelist=[], senderBlacklist=[], chatWhitelist=[], chatBlacklist=[]):

        super(Accordance, self).__init__()

        self.text = text
        self.func = func
        self.ifNotAuthorized = ifNotAuthorized

        self.data = None

        self.quick = quick

        self.isEnable = isEnable
        self.enableArgument = enableArgument

        self.senderWhitelist = senderWhitelist
        self.senderBlacklist = senderBlacklist

        self.chatWhitelist = chatWhitelist
        self.chatBlacklist = chatBlacklist

        self.logger = None

    def log(self, msg, level=logging.INFO):
        if self.logger is not None:
            if level == logging.DEBUG:
                self.logger.debug(msg)
            elif level == logging.INFO:
                self.logger.info(msg)
            elif level == logging.WARNING:
                self.logger.warning(msg)

    def run(self, func=None):
        if func is None:
            func = self.func

        if self.isEnable:
            self.log('Run accordance.')
            if self.enableArgument:
                func(self)
            else:
                func()
            return True
        else:
            self.log(f'Accordance not run. [isEnable={self.isEnable}]', logging.WARNING)
            return False

    def authorization(self, penger=None):
        authorizedSender = []
        authorizedChat = []
        blockedSender = []
        blockedChat = []

        mSender = None
        pSenderList = []
        gSenderWhitelist = []
        mChat = None
        pChatList = []
        gChatWhitelist = []

        if penger is not None:
            mSender = penger.mainSender
            pSenderList = penger.privateSenderList
            gSenderWhitelist = penger.senderWhitelist
            mChat = penger.mainChat
            pChatList = penger.privateChatList
            gChatWhitelist = penger.chatWhitelist

        senderANDchatQuick = self.quick.split(':')
        senderQuick = senderANDchatQuick[0].split(',')
        chatQuick = senderANDchatQuick[1].split(',')

        blockedSender.extend(self.senderBlacklist)
        blockedChat.extend(self.chatBlacklist)

        if 'all' in senderQuick:
            authorizedSender.append('all')
        else:
            if 'main' in senderQuick:
                if mSender is not None:
                    authorizedSender.append(mSender)
            if 'private' in senderQuick:
                authorizedSender.extend(pSenderList)
            if 'gWhitelist' in senderQuick:
                authorizedSender.extend(gSenderWhitelist)
            if 'whitelist' in senderQuick:
                authorizedSender.extend(self.senderWhitelist)

            if '-main' in senderQuick:
                if mChat is not None:
                    authorizedSender.append(mChat)
            if '-private' in senderQuick:
                authorizedSender.extend(pChatList)
            if '-gWhitelist' in senderQuick:
                authorizedSender.extend(gChatWhitelist)
            if '-whitelist' in senderQuick:
                authorizedSender.extend(self.chatWhitelist)

        if 'all' in chatQuick:
            authorizedChat.append('all')
        else:
            if 'main' in chatQuick:
                if mChat is not None:
                    authorizedChat.append(mChat)
            if 'private' in chatQuick:
                authorizedChat.extend(pChatList)
            if 'gWhitelist' in chatQuick:
                authorizedChat.extend(gChatWhitelist)
            if 'whitelist' in chatQuick:
                authorizedChat.extend(self.chatWhitelist)

            if '-main' in chatQuick:
                if mSender is not None:
                    authorizedChat.append(mSender)
            if '-private' in chatQuick:
                authorizedChat.extend(pSenderList)
            if '-gWhitelist' in chatQuick:
                authorizedChat.extend(gSenderWhitelist)
            if '-whitelist' in chatQuick:
                authorizedChat.extend(self.senderWhitelist)



        return authorizedSender, authorizedChat, blockedSender, blockedChat

    def check(self, ID, penger=None, LIST='sender'):
        authorizedSender, authorizedChat, blockedSender, blockedChat = self.authorization(penger)

        if LIST == 'sender':
            if ID in authorizedSender:
                return True
        elif LIST == 'chat':
            if ID in authorizedChat:
                return True
        elif LIST == 'sender&chat':
            if ID in authorizedSender and ID in authorizedChat:
                return True
        elif LIST == 'bSender':
            if ID in blockedSender:
                return True
        elif LIST == 'bChat':
            if ID in blockedChat:
                return True

        return False

    def checkAndRun(self, penger=None, data=None, senderID=None, chatID=None, hash=None, isEmptyAccordance=False):
        status = False

        if hash is None:
            hash = '{0:010x}'.format(int(time.time() * 256))[4:]

        if penger is not None:
            self.logger = penger.logger.getChild(f'Accordance-{hash}')
            self.logger.info(f'Start check and run accordance. [AccordanceText={self.text}]')

        if senderID is not None and chatID is None:
            self.log('Write Chat the same as Sender.', logging.DEBUG)
            chatID = senderID
        elif chatID is not None and senderID is None:
            self.log('Write Sender the same as Chat.', logging.DEBUG)
            senderID = chatID
        elif senderID is None and chatID is None and data is not None:
            self.log('Write Sender and Chat from Data.', logging.DEBUG)
            senderID = data['sender_id']
            chatID = data['chat_id']
        elif data is None and senderID is None and chatID is None:
            self.log('DATA and Sender and Chat are None.', logging.WARNING)
            return status

        self.data = data

        authorizedSender, authorizedChat, blockedSender, blockedChat = self.authorization(penger)

        self.log(f'[authorizedSender={authorizedSender}]', logging.DEBUG)
        self.log(f'[authorizedChat={authorizedChat}]', logging.DEBUG)
        self.log(f'[blockedSender={blockedSender}]', logging.DEBUG)
        self.log(f'[blockedChat={blockedChat}]', logging.DEBUG)

        if senderID not in blockedSender and chatID not in blockedChat:
            if (authorizedSender[0] == 'all' and authorizedChat[0] == 'all') or \
                    (authorizedSender[0] == 'all' and chatID in authorizedChat) or \
                    (senderID in authorizedSender and authorizedChat[0] == 'all') or \
                    (senderID in authorizedSender and chatID in authorizedChat):
                self.log('Sender and/or Chat are authorized.')
                self.log('Run the Accordance...')
                status = self.run()
                self.log(f'Run status: {status}')
            else:
                self.log('Sender and/or Chat are not authorized.', logging.WARNING)
                print(9999)
                if self.ifNotAuthorized is not None:
                    print(123123123)
                    if str(type(self.ifNotAuthorized)) == "<class 'penger.Accordance'>":
                        self.log('Redirect to other Accordance (ifNotAuthorized)...')
                        self.ifNotAuthorized.checkAndRun(penger=penger, data=data)
                    else:
                        self.log('Redirect to accordance (ifNotAuthorized)...')
                        self.run(func=self.ifNotAuthorized)
                elif penger is not None and not isEmptyAccordance:
                    self.log('Redirect to the empty accordance...')
                    penger.startEmptyAccordance(data)
        else:
            self.log('Sender and/or Chat are blocked.', logging.WARNING)
