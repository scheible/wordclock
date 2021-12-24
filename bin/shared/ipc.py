import json, zmq

NEW_JSON_UPDATE = 0
DATA_QUERY = 1
NO_JSON_AVAILABLE = 2
MALFORMED_JSON = 3
NEW_JSON_REMOVE = 4
NEW_JSON_ADD = 5

class WebserverComponentIpcListener():
    def __init__(self, timeout=5000):
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.SUB)
        self.__socket.connect("tcp://localhost:6666")
        self.__socket.subscribe(b'')
        self.__socket.RCVTIMEO = timeout

    def recv(self):
        try:
            m = self.__socket.recv()
            return NEW_JSON_UPDATE, m.decode('UTF-8')
        except zmq.error.Again:
            return NO_JSON_AVAILABLE, None
        except json.JSONDecodeError:
            return MALFORMED_JSON, None


class WebserverComponentIpcSender():
    def __init__(self):
        self.__host = 'localhost'
        self.__port = 1234
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REQ)
        self.__socket.RCVTIMEO = 500
        self.__socket.setsockopt(zmq.LINGER, 500)
        self.__socket.connect('tcp://' + self.__host + ':' + str(self.__port))

    def send(self, jsonStringData):
        try:
            self.__socket.send(jsonStringData.encode('UTF-8'))
            rcv = self.__socket.recv()
            return rcv.decode('UTF-8')
        except zmq.error.Again as e:
            return "error. no answer from wordclock daemon."


class DaemonComponentIpcBindung():
    def __init__(self):
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REP)
        self.__socket.RCVTIMEO = 5000
        self.__socket.setsockopt(zmq.LINGER, 5000)
        #self.__socket.bind('tcp://*:1234')

        self.__pubContext = zmq.Context()
        self.__pubSocket = self.__pubContext.socket(zmq.PUB)
        #self.__pubSocket.bind("tcp://*:6666")


    def receiveCommand(self, state):
        try:
            obj = self.__recvJson()

            if (obj['commandType'] == 'query'):
                self.__sendJson(state)
                return DATA_QUERY, None

            elif (obj['commandType'] == 'set'):
                dataObj = obj['dat']
                self.__returnOk()
                return NEW_JSON_UPDATE, dataObj

            elif (obj['commandType'] == 'remove'):
                dataObj = obj['dat']
                self.__returnOk()
                return NEW_JSON_REMOVE, dataObj

            elif (obj['commandType'] == 'add'):
                dataObj = obj['dat']
                self.__returnOk()
                return NEW_JSON_ADD, dataObj

        except zmq.error.Again as e:
            return NO_JSON_AVAILABLE, None

        except (json.JSONDecodeError, TypeError):
            self.__returnNotOk(MALFORMED_JSON)
            return MALFORMED_JSON, None

        except:
            self.__returnNotOk(MALFORMED_JSON)
            return MALFORMED_JSON, None



    def sendCommand(self, jsonConfig):
        obj = jsonConfig
        self.__publishJson(obj)


    def __returnOk(self):
        obj = {'state': 'ok'}
        try:
            self.__sendJson(obj)
        except zmq.error.Again as e:
            pass


    def __returnNotOk(self, errorCode):
        obj = {'state': 'failed', 'errorCode': errorCode}
        try:
            self.__sendJson(obj)
        except zmq.error.Again as e:
            pass


    def __publishJson(self, obj):
        self.__pubSocket.send(json.dumps(obj).encode('UTF-8'))


    def __sendJson(self, obj):
        self.__socket.send(json.dumps(obj).encode('UTF-8'))


    def __recvJson(self):
        message = self.__socket.recv(flags=zmq.NOBLOCK)
        obj = json.loads(message.decode('UTF-8'))
        return obj
