# ----------------------------------------------------------------------------------------
# Penger
#
# A Telegram Bot API Library for python with a flexible command access control system.
# This library is being developed for service informer bots.
#
# Author: Terminator (https://github.com/fresh-ter)
#
# Copyright (c) 2020 Penguins of Madagascar
#
# Released under MIT License (MIT)
# ----------------------------------------------------------------------------------------


import random
import logging
import requests


def getHash():
    """This function generates a random hash.

    Returns:
        str: A hash (6 characters in string). Example: 'e55e99'.

    """
    return '{0:010x}'.format(hash(random.random()))[:6]


class Penger(object):
    """Penger

    All the most basic things happen here:
    * sending messages or images;
    * receiving updates from the Telegram server;
    * responding to them;
    * searching for the necessary Accordance;
    * blocking chat and senders IDs at the global level;
    * and much more;

    Attributes:
        token (str): A token for Telegram Bot API. Default to 'None'.
        apiAddress (str): The address for building requests to the Telegram server.
                            Defaults to "https://api.telegram.org/".

        response (str | None): A response from the Telegram server. Defaults to None.
        updateID (int): An ID of the update to start processing incoming updates from the Telegram server.
                        Defaults to 0.

        mainSender (int | None): An ID of main sender. Defaults to None.
        privateSenderList (list[int]): A private list of sender IDs. Defaults to [].
        senderWhitelist (list[int]): A special list of allowed sender IDs. Defaults to [].
        senderBlacklist (list[int]): A list of blocked sender IDs. Defaults to [].

        mainChat (int | None): An ID of main chat. Defaults to None.
        privateChatList (list[int]): A private list of chat IDs. Defaults to [].
        chatWhitelist (list[int]): A special list of allowed chat IDs. Defaults to [].
        chatBlacklist (list[int]): A list of blocked chat IDs. Defaults to [].

        accordance (list[Accordance] | dict): An array of Accordance between a command and a function. Defaults to [].
        emptyAccordance (Accordance | function | None): An empty Accordance between a empty (unknown) command and
                                                        a function. Defaults to [].

    """

    def __init__(self, token='None', updateID=0,
                 mainSender=None, privateSenderList=None, senderWhitelist=None, senderBlacklist=None,
                 mainChat=None, privateChatList=None, chatWhitelist=None, chatBlacklist=None,
                 accordance=None, emptyAccordance=None,
                 loggingFile='penger.log', loggingFilemode='a', loggingLevel=logging.INFO,
                 loggingFormat='[%(asctime)s]# %(levelname)-8s %(name)s: %(message)s'):

        """Constructor of Penger class

        Here:
        * initialization the values of attributes of the Penger class;
        * configuring the logging library for further work.

        Args:
            token (str): Described in a docstring of Penger class.
            updateID (int): Described in a docstring of Penger class.

            mainSender (int | None): Described in a docstring of Penger class. Defaults to None.
            privateSenderList (list[int]): Described in a docstring of Penger class. Defaults to None
            senderWhitelist (list[int]): Described in a docstring of Penger class. Defaults to None.
            senderBlacklist (list[int]): Described in a docstring of Penger class. Defaults to None.

            mainChat: Described in a docstring of Penger class. Defaults to None.
            privateChatList: Described in a docstring of Penger class. Defaults to None.
            chatWhitelist: Described in a docstring of Penger class. Defaults to None.
            chatBlacklist: Described in a docstring of Penger class. Defaults to None.

            accordance: Described in a docstring of Penger class. Defaults to None.
            emptyAccordance: Described in a docstring of Penger class. Defaults to None.

            loggingFile (str): A name/address of the file to loggging. Defaults to "penger.log".
            loggingFilemode (str): A file opening mode.
                                    'a' - appending to the end of the file if it exists.
                                    'w' - truncating the file first.
                                    Defaults to "a".
            loggingLevel (int): A logging level for the logging library. Defaults to logging.INFO (20).
            loggingFormat (str): A logging format for the logging library.
                                    Defaults to "[%(asctime)s]# %(levelname)-8s %(name)s: %(message)s".

        """
        super(Penger, self).__init__()

        #
        # Initialization the values of attributes of the Penger class.
        #

        if privateSenderList is None:
            privateSenderList = []
        if senderWhitelist is None:
            senderWhitelist = []
        if senderBlacklist is None:
            senderBlacklist = []

        if privateChatList is None:
            privateChatList = []
        if chatWhitelist is None:
            chatWhitelist = []
        if chatBlacklist is None:
            chatBlacklist = []

        if accordance is None:
            accordance = []

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

        #
        # Configuring the logging library for further work.
        #

        logging.basicConfig(filename=loggingFile, filemode=loggingFilemode, format=loggingFormat, level=loggingLevel)
        self.logger = logging.getLogger('Penger')

        self.logger.debug('Creating a Penger object.')

    def logStatus(self, status, logMessage):
        """This function write to the log <logMessage> and <status>.

        Args:
            status (bool): Some logical value.
            logMessage (str): Some message.

        Returns:
            bool: The value of the <status> variable.

        """
        if status:
            self.logger.info(logMessage + ' STATUS: ' + str(status))
        else:
            self.logger.error(logMessage + ' STATUS: ' + str(status))
        return status

    def test(self):
        """ This function is a simple test.

        Returns:
            bool: True

        """
        return self.logStatus(True, 'This is Penger-test.')

    def isSuccessfulRequest(self):
        """This function is needed to check the success of the request.

        Note:
            The response contains a JSON object, which always has a Boolean field 'ok' and may have an optional String
            field 'description' with a human-readable description of the result. If 'ok' equals true, the request was
            successful and the result of the query can be found in the 'result' field. In case of an unsuccessful
            request, 'ok' equals false and the error is explained in the 'description'.

        Returns:
            bool: The status of the saved response written to the <self.response> variable

        """
        return self.response.json()['ok']

    def makeRequest(self, method, parameters=None, files=None):
        """This function generates and sends an api request to the Telegram server.

        Args:
            method (str): Method to the Telegram Bot API.
            parameters (dict | None): Parameters of the method. Defaults to None.
            files (None | dict): File object in dictionary. Defaults to None.

        Returns:
            bool: The status of the response.

        """
        self.response = requests.post(self.apiAddress + 'bot' + self.token + '/' + method, data=parameters,
                                      files=files)
        return self.isSuccessfulRequest()

    def sendMessage(self, chat_id, text, disable_notification=False, parse_mode=False):
        """Sending a text to the specified chat ID.

        Args:
            chat_id (int | str): Unique identifier for the target chat or
                                    username of the target channel (in the format @channelusername).
            text (str): Text of the message to be sent, 1-4096 characters after entities parsing.
            disable_notification (bool): Sends the message silently. Users will receive a notification with no sound.
            parse_mode (bool): TODO

        Returns:
            bool: The status of sending message.

        """
        if chat_id == 'mainC':  # TODO
            chat_id = self.mainChat
        parameters = {'chat_id': chat_id, 'text': text, 'disable_notification': disable_notification}

        return self.logStatus(self.makeRequest('sendMessage', parameters),
                              f'Sending message. chat_id: {chat_id}, notification: {not disable_notification}.')

    def sendMessageToMainChat(self, text, disable_notification=False, parse_mode=False):
        """Sending a text to the main chat.

        Args:
            text (str): Text of the message to be sent, 1-4096 characters after entities parsing.
            disable_notification (bool): Sends the message silently. Users will receive a notification with no sound.
            parse_mode (bool): TODO

        Returns:
            bool: The status of sending message.

        """
        return self.sendMessage(self.mainChat, text, disable_notification, parse_mode)

    def sendMessageToChat(self, data, text, disable_notification=False, parse_mode=False):
        """Sending a text to the the specified chat ID.

        The chat ID is taken from the <data> dictionary.

        Args:
            data (dict): This dictionary must have a chat ID or username with the key 'chat_id'.
            text (str): Text of the message to be sent, 1-4096 characters after entities parsing.
            disable_notification (bool): Sends the message silently. Users will receive a notification with no sound.
            parse_mode (bool): TODO

        Returns:
            bool: The status of sending image.

        """
        return self.sendMessage(data['chat_id'], text, disable_notification, parse_mode)

    def sendImage(self, chat_id, image, text=None, disable_notification=False, parse_mode=False):
        """Sending an image to the the specified chat ID.

        Args:
            chat_id (int | str): Unique identifier for the target chat or
                                    username of the target channel (in the format @channelusername).
            image (object): File object. (For example: image = open('picture.png'))
            text (str): Photo caption, 0-1024 characters after entities parsing. Defaults to None.
            disable_notification (bool): Sends the message silently. Users will receive a notification with no sound.
            parse_mode (bool): TODO

        Returns:
            bool: The status of sending image.

        """
        files = {'photo': image}
        parameters = {'chat_id': chat_id, 'caption': text, 'disable_notification': disable_notification}

        return self.logStatus(self.makeRequest('sendPhoto', parameters, files),
                              f'Sending image to chat_id: {chat_id}, notification: {not disable_notification}.')

    def getDataFromUpdate(self, updateJSON):  # TODO: make static
        """Parsing the update from the Telegram server for the bot.

        Args:
            updateJSON (dict): json data of one update received in the response from the Telegram server.

        Returns:
            dict: Dictionary with the necessary data (chat ID, sender ID, text etc).

        """
        data = {'update_id': updateJSON['update_id'], 'sender_id': updateJSON['message']['from']['id'],
                'chat_id': updateJSON['message']['chat']['id'], 'text': updateJSON['message']['text']}

        return data

    def startEmptyAccordance(self, data, hashHex=None):
        """Starting an empty Accordance.

        First, we check whether the empty Accordance is an object of the Accordance class.
        If yes, we pass the object a pointer to self and a dictionary with data. We also run the check function.
        Else, run the function and pass the dictionary with data to it.

        Args:
            data (dict): Dictionary with the necessary data (chat ID, sender ID, text etc).
            hashHex (str): A random hash.

        Returns:
            bool: The status of run empty Accordance.

        """
        if hashHex is None:
            hashHex = getHash()

        status = False

        if self.emptyAccordance is not None:
            if isinstance(self.emptyAccordance, Accordance):
                self.logger.info(f'Start check of the empty Accordance-{hashHex}...')
                status = self.emptyAccordance.checkAndRun(penger=self, data=data)
                self.logger.info(f'End check of the empty Accordance-{hashHex}.')
            else:
                self.logger.info('Start of the empty accordance (base function)...')
                self.emptyAccordance(data)
                status = True
                self.logger.info('End of the empty accordance (base function).')

        return status

    def searchAndStartAccordance(self, data):
        """Searching and starting an Accordance.

        Here we search for the appropriate Accordance in the array by text.

        First, we check whether the Accordance is an object of the Accordance class.
        If yes, we pass the object a pointer to self and a dictionary with data. We also run the check function.
        Else, run the function and pass the dictionary with data to it.

        Args:
            data (dict): Dictionary with the necessary data (chat ID, sender ID, text etc).

        Returns:
            bool: The status of run Accordance.

        """
        # TODO comment
        status = False
        hashHex = getHash()

        for acc in self.accordance:
            if isinstance(acc, Accordance):
                if data['text'].startswith(acc.command + " ") or data["text"] == acc.command:
                    self.logger.info(f'Start of the Accordance-{hashHex}...')
                    status = acc.checkAndRun(penger=self, data=data, hashHex=hashHex)
                    self.logger.info(f'End of the Accordance-{hashHex}.')
            else:
                if data['text'].startswith(acc + " ") or data["text"] == acc:
                    self.logger.info('Start of the accordance (from dict)...')
                    self.accordance[acc](data)
                    status = True
                    self.logger.info('End of the accordance (from dict).')
            if status:
                return status
            hashHex = getHash()

        # If the correct Accordance is not found, then start an empty Accordance.
        if not status:
            status = self.startEmptyAccordance(data, hashHex)

        return status

    def respondToMessage(self, updateJSON):
        """This function responds to incoming messages.

        This checks whether the sender and chat IDs are blacklisted.
        If Yes, the Accordance search is not performed.

        Args:
            updateJSON (dict): json data of one update received in the response from the Telegram server.

        """
        data = self.getDataFromUpdate(updateJSON)

        if data['sender_id'] not in self.senderBlacklist and data['chat_id'] not in self.chatBlacklist:
            self.logger.debug('Start search accordance.')
            self.searchAndStartAccordance(data)
        else:
            self.logger.warning('Sender and/or Chat blocked.')

    def updateAndRespond(self):
        """This function downloads updates from the Telegram server and responds to them.

        Only messages are responded.

        Returns:
            bool: The status of getting updates.

        """
        status = self.logStatus(self.makeRequest('getUpdates'),
                                'Getting updates.')
        updatesJSON = self.response.json()

        if self.updateID == 0:
            # Skipping all updates.
            self.updateID = updatesJSON['result'][len(updatesJSON['result']) - 1]['update_id']

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
    def __init__(self, command, func, quick='all:all', isEnable=True, enableArgument=False, ifNotAuthorized=None,
                 senderWhitelist=None, senderBlacklist=None, chatWhitelist=None, chatBlacklist=None):

        super(Accordance, self).__init__()

        if senderWhitelist is None:
            senderWhitelist = []
        if senderBlacklist is None:
            senderBlacklist = []

        if chatWhitelist is None:
            chatWhitelist = []
        if chatBlacklist is None:
            chatBlacklist = []

        self.command = command

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
            self.log('Run the Accordance...')
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

    def checkAndRun(self, penger=None, data=None, senderID=None, chatID=None, hashHex=None):
        status = False

        if hashHex is None:
            hashHex = getHash()

        if penger is not None:
            self.logger = penger.logger.getChild(f'Accordance-{hashHex}')
            self.logger.info(f'Start check and run accordance. [AccordanceCommand={self.command}] [{self.quick}]')

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
                status = self.run()
                self.log(f'Run status: {status}')
                status = True
            else:
                self.log('Sender and/or Chat are not authorized.', logging.WARNING)
                if self.ifNotAuthorized is not None:
                    if str(type(self.ifNotAuthorized)) == "<class 'penger.Accordance'>":
                        self.log('Redirect to other Accordance (ifNotAuthorized)...')
                        status = self.ifNotAuthorized.checkAndRun(penger=penger, data=data)
                    else:
                        self.log('Redirect to accordance (ifNotAuthorized)...')
                        self.run(func=self.ifNotAuthorized)
        else:
            self.log('Sender and/or Chat are blocked.', logging.WARNING)

        return status
