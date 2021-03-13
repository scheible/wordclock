import board
import neopixel
import time
import math
from threading import Thread, Lock
from queue import Queue
import random

# use setPixel method to configure the LED matrix
# then call flush to output the configuration on the
# actual LEDs. When a number > 0 is specified, the
# LED matrix will change gradually to the new state
#
# If the LED matrix was still in transition when
# flush is called, the current transition is aborted
# and the new transistion is executed from the current
# state into the new state

class MatrixDriver():

	def __init__(self):
		self.__cols = 11
		self.__rows = 20
		self.__numLeds = self.__cols * self.__rows
		self.__currentMatrix = neopixel.NeoPixel(board.D18, self.__numLeds, auto_write=False)
		self.__startMatrix = [(0,0,0)]*self.__numLeds
		self.__targetMatrix = [(0,0,0)]*self.__numLeds
		self.__configMatrix = [(0,0,0)] *self.__numLeds
		self.__animationLock = Lock()
		self.__transitionThread = Thread()
		self.__stopQueue = Queue(maxsize=0)

	def getPixelIndex(self, x, y):
		if (x % 2 == 1):
			index = self.__numLeds - ((x+1)*self.__rows) + y
		else:
			index = self.__numLeds - (x*self.__rows) - y - 1

		return index

	def getTransitionAt(self, start, target, steps, t):
		# linear
		#y = start + ( (target-start) / steps) * t

		#exponential
		start += 1
		target += 1
		b = math.log(target/start)/steps
		a = target / math.exp(b*steps)
		y = a * math.exp(b*t)
		return int(y-1)

	def getTransitionAtForTupble(self, start, target, steps, t):
		new = ()
		for i in range(0, 3):
			value = self.getTransitionAt(start[i], target[i], steps, t)
			new += (value,)

		return new

	def transition(self, steps):
		self.__animationLock.acquire()

		for i in range(0, self.__numLeds):
			self.__startMatrix[i] = self.__currentMatrix[i].copy()

		for t in range(0, steps):
			for i in range(0, self.__numLeds):
				start = self.__startMatrix[i]
				target = self.__targetMatrix[i]
				newCurrent = self.getTransitionAtForTupble(start, target, steps, t)
				self.__currentMatrix[i] = newCurrent

			try:
				message = self.__stopQueue.get(block=False)
				self.__stopQueue.task_done()
				if (message == "stop"):
					break
			except:
				pass

			time.sleep(0.005)
			self.__currentMatrix.show()

		for i in range(0, self.__numLeds):
			self.__targetMatrix[i] = (0, 0, 0)

		self.__animationLock.release()

	def nonBlockingTransition(self, steps):
		if (not self.__transitionThread.is_alive()):
			self.__transitionThread = Thread(target=self.transition, args=(steps,))
			self.__transitionThread.start()
		else:
			print("old animation still running")

	def setPixel(self, x, y, rgb):
		self.__configMatrix[self.getPixelIndex(x,y)] = rgb

	def getPixel(self, x, y):
		return self.__configMatrix[self.getPixelIndex(x,y)]	

	def getLetter(self, x, y):
		y = y * 2

		return self.__configMatrix[self.getPixelIndex(x,y)]

	def getCurrentPixel(self, x, y):
		return self.__currentMatrix[self.getPixelIndex(x,y)]

	def setLetter(self, x, y, rgb):
		y = y * 2

		self.__configMatrix[self.getPixelIndex(x,y)] = rgb
		self.__configMatrix[self.getPixelIndex(x,y+1)] = rgb


	def flush(self, transition=0):
		# transition 0 means directly flush
		
		# check if there is a transition running
		# if yes, try to cancel it and wait
		if (self.__transitionThread.is_alive()):
			self.__stopQueue.put("stop")
			self.__transitionThread.join()


		# copy configMatrix into targetMatrix
		self.__animationLock.acquire()

		if (transition > 0):
			for i in range(0, self.__numLeds):
				self.__targetMatrix[i] = self.__configMatrix[i]
				self.__configMatrix[i] = (0, 0, 0)
			self.__animationLock.release()
			self.nonBlockingTransition(transition)

		else:
			for i in range(0, self.__numLeds):
				self.__currentMatrix[i] = self.__configMatrix[i]
				self.__configMatrix[i] = (0, 0, 0)
			self.__animationLock.release()
			self.__currentMatrix.show()

	def waitForTransition(self):
		self.__animationLock.acquire()
		self.__animationLock.release()
		
def whatsapp():
	for y in range(0,20):
		for x in range(0,11):
			driver.setPixel(x,y, (0,10,0))
	driver.flush(30)

	for i in range(0, 5):
		b= 5
		if (i%2==0):
			b = 70

		for y in range(0,20):
			for x in range(0,11):
				driver.setPixel(x,y, (0,b,0))
		driver.flush(30)
		driver.waitForTransition()


def matrix():
	rgb = (70, 0, 0)

	stop = False
	c = 0

	while True:
		if (stop):
			c += 1
		if (c > 20):
			break

		try:
			for row in range(0, 20):
				for col in range(0,11):

					if (row == 0):
						r = random.randint(0,3)
						if (r < 1 and not stop):
							driver.setPixel(col, 0, rgb)
					else:
						driver.setPixel(col, row, driver.getCurrentPixel(col,row-1))
				
			driver.flush()
			time.sleep(0.12)
		except KeyboardInterrupt:
			stop = True


def randColor():
	while True:
		try:
			for row in range(0, 10):
				for col in range(0,11):

					rgb = (random.randint(0,80), random.randint(0,30), random.randint(0,20))
					driver.setLetter(col, row, rgb)
				
			driver.flush(30)
			driver.waitForTransition()
		except KeyboardInterrupt:
			break


def hour(h):

	if (h == 0):
		ZWOELF()
	elif (h == 1):
		EIN()
	elif (h == 2):
		ZWEI()
	elif (h == 3):
		DREI()
	elif (h == 4):
		VIER()
	elif (h == 5):
		FUENF2()
	elif (h == 6):
		SECHS()
	elif (h == 7):
		SIEBEN()
	elif (h == 8):
		ACHT()
	elif (h == 9):
		NEUN()
	elif (h == 10):
		ZEHN2()
	elif (h == 11):
		ELF()
	elif (h == 12):
		ZWOELF()

def showTime(hh, mm):
	ES()
	IST()


	if (mm < 5):
		pass
	elif (mm < 10):
		FUENF1()
		NACH()
	elif (mm < 15):
		ZEHN1()
		NACH()
	elif (mm < 20):
		VIERTEL()
		NACH()
	elif (mm < 25):
		ZWANZIG()
		NACH()
	elif (mm < 30):
		FUENF1()
		VOR()
		HALB()
	elif (mm < 35):
		HALB()
	elif (mm < 40):
		FUENF1()
		NACH()
		HALB()
	elif (mm < 45):
		ZEHN1()
		NACH()
		HALB()
	elif (mm < 50):
		DREIVIERTEL()
	elif (mm < 55):
		ZEHN1()
		VOR()
	else:
		FUENF1()
		VOR()


	if (mm >= 00 and mm < 25):
		hour(hh % 12)
	else:
		hour((hh+1)	 % 12)

	if (mm < 5):
		UHR()


	driver.flush(60)



def ES():
	wordOn(0, 0, 2)

def IST():
	wordOn(0, 3, 3)

def FUENF1():
	wordOn(0, 7, 4)

def ZEHN1():
	wordOn(1, 0, 4)

def VIERTEL():
	wordOn(2, 4, 7)

def ZWANZIG():
	wordOn(1, 4, 7)

def DREIVIERTEL():
	wordOn(2, 0, 11)

def VOR():
	wordOn(3, 0, 3)

def NACH():
	wordOn(3, 7, 4)

def HALB():
	wordOn(4, 0, 4)

def UHR():
	wordOn(9, 8, 3)

def EIN():
	wordOn(5, 0, 3)

def ZWEI():
	wordOn(5, 7, 4)

def DREI():
	wordOn(6, 0, 4)

def VIER():
	wordOn(6, 7, 4)

def FUENF2():
	wordOn(4, 7, 4)

def SECHS():
	wordOn(7, 0, 5)

def SIEBEN():
	wordOn(8, 0, 6)

def ACHT():
	wordOn(7, 7, 4)

def NEUN():
	wordOn(9, 3, 4)

def ZEHN2():
	wordOn(9, 0, 4)

def ELF():
	wordOn(4, 5, 3)

def ZWOELF():
	wordOn(8, 6, 5)


def on(x, y):
	global rgbCol
	driver.setLetter(x,y, rgbCol)


def wordOn(line, start, length):
	for i in range(start, start+length):
		on(i, line)




driver = MatrixDriver()


matrix()
randColor()
exit()

#for y in range(0,20):
#	for x in range(0,11):
#		driver.setPixel(x,y, (30,30,30))
#		driver.flush()
#		time.sleep(0.1)

rgbCol = (140, 0 , 0)
showTime(3, 15)
time.sleep(3)
rgbCol = (140, 140 , 0)
showTime(3,20)

time.sleep(5)
whatsapp()
showTime(3,20)

time.sleep(3)
rgbCol = (0, 140 , 0)
showTime(3,25)
time.sleep(3)
rgbCol = (0, 0 , 140)
showTime(3,30)