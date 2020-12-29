from tkinter import *
import tkinter.font as TkFont
from time import sleep

class Letter:

	def __init__(self, letter, color, x, y):
		self._letter = letter
		self._color = color
		self._x = x
		self._y = y

	def getLetter(self):
		return self._letter

	def setColor(self, color):
		self._color = color

	def getColor(self):
		return self._color

	def setX(self, x):
		self._x = x

	def getX(self):
		return self._x

	def setY(sefl, y):
		self._y = y

	def getY(self):
		return self._y


class Demonstrator:

	def __init__(self, master):

		pattern = \
		[ 'ESKISTAFÜNF', \
		  'ZEHNZWANZIG', \
		  'DREIVIERTEL', \
		  'VORFUNKNACH', \
		  'HALBAELFÜNF', \
		  'EINSXAMZWEI', \
		  'DREIPMJVIER', \
		  'SECHSNLACHT', \
		  'SIEBENZWÖLF', \
		  'ZEHNEUNKUHR']

		self.letters = []

		for y, line in enumerate(pattern):
			for x, letter in enumerate(line):
				self.letters.append(Letter(letter, '#aaaaaa', x, y))

		canvas_width = 700
		canvas_height = 700
		self.w = Canvas(master,width=canvas_width,height=canvas_height)
		self.w.pack()
		self.w.delete("all")


		self.border_x = 100
		self.border_y = 100
		self.width = canvas_width - (2* self.border_x)
		self.height = canvas_height - (2* self.border_y)
		self.step_x = self.width / 11
		self.step_y = self.height / 10

		self.render()

	def setColor(self, x, y, color):
		for l in self.letters:
			if (l.getX() == x and l.getY() == y):
				l.setColor(color)
				break

	def render(self):
		#self.drawGrid("#999999")

		self.renderLetters(self.letters)

	def setLetter(self, x, y, letter, color):
		pos_x = self.border_x + (x*self.step_x + (self.step_x/2))
		pos_y = self.border_y + (y*self.step_y + (self.step_y/2))
		helv36 = TkFont.Font(family='Helvetica',size=12, weight='normal')
		self.w.create_text(pos_x, pos_y, text=letter, fill=color, font=helv36)

	def renderLetters(self, letters):
		for l in letters:
			self.setLetter(l.getX(), l.getY(), l.getLetter(), l.getColor())

	def drawGrid(self, color):
		for i in range(0,12):
			self.w.create_line(i*self.step_x+self.border_x, self.border_y, i*self.step_x+self.border_x, self.height+self.border_y, fill=color)

		for i in range(0,11):
			self.w.create_line(self.border_x, i*self.step_y+self.border_y, self.width+self.border_x, i*self.step_y+self.border_y, fill=color)	


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

def tick():
	allOff()
	mm = 00
	hh = 15
	ES()
	IST()


	if (mm < 10):
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


	demo.render()
	global onCounter
	print(onCounter)
	#master.after(1000, tick)



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
	global onCounter
	onCounter+=1
	demo.setColor(x, y, '#ff0000')

def wordOn(line, start, length):
	for i in range(start, start+length):
		on(i, line)

def allOff():
	for x in range(0, 12):
		for y in range(0, 11):
			off(x, y)

def off(x, y):
	demo.setColor(x, y, '#aaaaaa')

onCounter = 0
master = Tk()
demo = Demonstrator(master)
master.after(10, tick)


mainloop()