#
# the labersack module shall enable interprocess communication
# using zmq library and define the messages that are exchanged.
#
# The deamon is considered the server 
# and the web app is considered the client

import zmq

COMMAND_SET_LETTER_COLOR = b'SLC'
COMMAND_GET_LETTER_COLOR = b'GLC'
COMMAND_SET_FRAME_COLOR  = b'SFC'
COMMAND_GET_FRAME_COLOR  = b'GFC'
COMMAND_SET_MINUTES_COLOR = b'SMC'
COMMAND_GET_MINUTES_COLOR = b'GMC'
COMMAND_SET_SECONDS_COLOR = b'SSC'
COMMAND_GET_SECONDS_COLOR = b'GSC'
COMMAND_SET_BRIGHTNESS = b'SBR'
COMMAND_GET_BRIGHTNESS = b'GBR'

COMMAND_OK = b'K'
COMMAND_NOT_OK = b'N'

class EventClient():
	def __init__(self):
		self.__context = zmq.Context()
		self.__socket = self.__context.socket(zmq.SUB)
		self.__socket.connect("tcp://localhost:6666")
		self.__socket.subscribe(b'UPD')
		self.__socket.RCVTIMEO = 5000

	def tickUpdate(self):
		try:
			m = self.__socket.recv()
			return True
		except:
			return False


class Client():
	def __init__(self):
		self.__host = 'localhost'
		self.__port = 1234
		self.__context = zmq.Context()
		self.__socket = self.__context.socket(zmq.REQ)
		self.__socket.RCVTIMEO = 1200
		self.__socket.setsockopt(zmq.LINGER, 500)
		self.__socket.connect('tcp://' + self.__host + ':' + str(self.__port))

	def __getColor(self, command):
		self.__socket.send(command, flags=zmq.NOBLOCK)

		try:
			returnValue = self.__socket.recv()
			if (len(returnValue) >= 3):
				red = returnValue[0]
				green = returnValue[1]
				blue = returnValue[2]
				return red, green, blue
			else:
				return None, None, None
		except Exception as e:
			return None, None, None

	def __setColor(self, command, r, g, b):
		message = bytearray(command)
		message.append(r % 256)
		message.append(g % 256)
		message.append(b % 256)
		self.__socket.send(message, flags=zmq.NOBLOCK)

		try:
			returnValue = self.__socket.recv()
			if (len(returnValue) > 0):
				return returnValue == COMMAND_OK
			else:
				return False
		except Exception as e:
			return False

	def __getValue(self, command):
		self.__socket.send(command, flags=zmq.NOBLOCK)

		try:
			returnValue = self.__socket.recv()
			if (len(returnValue) >= 1):
				return int(returnValue[0])
			else:
				return None
		except Exception as e:
			return None

	def __setValue(self, command, value):
		message = bytearray(command)
		message.append(value % 256)

		self.__socket.send(message, flags=zmq.NOBLOCK)

		try:
			returnValue = self.__socket.recv()
			if (len(returnValue) > 0):
				return returnValue == COMMAND_OK
			else:
				return False
		except Exception as e:
			return False

	def getLetterColor(self):
		return self.__getColor(COMMAND_GET_LETTER_COLOR)

	def setLetterColor(self, r, g, b):
		return self.__setColor(COMMAND_SET_LETTER_COLOR, r, g, b)

	def getFrameColor(self):
		return self.__getColor(COMMAND_GET_FRAME_COLOR)

	def setFrameColor(self, r, g, b):
		return self.__setColor(COMMAND_SET_FRAME_COLOR, r, g, b)

	def getMinutesColor(self):
		return self.__getColor(COMMAND_GET_MINUTES_COLOR)

	def setMinutesColor(self, r, g, b):
		return self.__setColor(COMMAND_SET_MINUTES_COLOR, r, g, b)

	def getSecondsColor(self):
		return self.__getColor(COMMAND_GET_SECONDS_COLOR)

	def setSecondsColor(self, r, g, b):
		return self.__setColor(COMMAND_SET_SECONDS_COLOR, r, g, b)

	def getBrightness(self):
		return self.__getValue(COMMAND_GET_BRIGHTNESS)

	def setBrightness(self, b):
		return self.__setValue(COMMAND_SET_BRIGHTNESS, b)

	def __del__(self):
		self.__context.destroy()


class Server():
	def __init__(self):
		self.__host = '*'
		self.__port = 1234
		self.__context = zmq.Context()
		self.__socket = self.__context.socket(zmq.REP)
		self.__socket.RCVTIMEO = 1000
		self.__socket.setsockopt(zmq.LINGER, 500)
		self.__socket.bind('tcp://' + self.__host + ':' + str(self.__port))

		self.__pubContext = zmq.Context()
		self.frameColor = [10, 20, 30]
		self.letterColor = [99, 199, 249]
		self.secondsColor = [0, 0, 0]
		self.minutesColor = [0, 0, 0]
		self.brightness = [2]	
		self.__pubSocket = self.__pubContext.socket(zmq.PUB)
		self.__pubSocket.bind("tcp://*:6666")

		self.__onChangeCallback = None

		self.frameColor = [10, 20, 30]
		self.letterColor = [99, 199, 249]
		self.secondsColor = [0, 0, 0]
		self.minutesColor = [0, 0, 0]
		self.brightness = [2]

	def poll(self):
		try:
			message = self.__socket.recv(flags=zmq.NOBLOCK)

			if (len(message) >= 3):
				params = message[3:]

				print(message[:3])

				if (message[:3] == COMMAND_SET_LETTER_COLOR):
					self.__setColor(self.letterColor, params)

				elif (message[:3] == COMMAND_GET_LETTER_COLOR):
					self.__getColor(self.letterColor)

				elif (message[:3] == COMMAND_SET_FRAME_COLOR):
					self.__setColor(self.frameColor, params)

				elif (message[:3] == COMMAND_GET_FRAME_COLOR):
					self.__getColor(self.frameColor)

				elif (message[:3] == COMMAND_SET_MINUTES_COLOR):
					self.__setColor(self.minutesColor, params)

				elif (message[:3] == COMMAND_GET_MINUTES_COLOR):
					self.__getColor(self.minutesColor)

				elif (message[:3] == COMMAND_SET_SECONDS_COLOR):
					self.__setColor(self.secondsColor, params)

				elif (message[:3] == COMMAND_GET_SECONDS_COLOR):
					self.__getColor(self.secondsColor)

				elif (message[:3] == COMMAND_SET_BRIGHTNESS):
					self.__setColor(self.brightness, params, 1)

				elif (message[:3] == COMMAND_GET_BRIGHTNESS):
					self.__getColor(self.brightness)

			else:
				self.__socket.send(COMMAND_NOT_OK)
				return False
			return True
		except Exception as e:
			return False

	def __setColor(self, colorPointer, params, expectedParams=3):
		if (len(params) >= expectedParams):
			for i, p in enumerate(params):
				colorPointer[i] = p;
			self.__socket.send(COMMAND_OK)
			self.__pubSocket.send(b'UPD')
			self.__onChangeCallback()
		else:
			self.__socket.send(COMMAND_NOT_OK)

	def __getColor(self, colorPointer):
		message = bytearray()
		for c in colorPointer:
			message.append(c)
		self.__socket.send(message)

	def setOnChangeCallback(self, callback):
		self.__onChangeCallback = callback
