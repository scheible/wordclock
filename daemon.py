from Drv_Qlock_Two.Drv_QlockTwo import *
from time import sleep
from datetime import datetime

json_qlocktwo_file_path = "Drv_Qlock_Two/cfg/Drv_QlockTwo.json"
json_ws2812b_file_path = "Drv_Qlock_Two/cfg/Drv_ws2812b.json"
drv_qlocktwo = Drv_QlockTwo(json_qlocktwo_file_path, json_ws2812b_file_path)
drv_qlocktwo.set_font_color([180, 180, 180])
old_mm = -1
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
	hh = datetime.now().hour
	mm = datetime.now().minute
	global old_mm
	if (mm == old_mm):
		return
	old_mm = mm
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


	drv_qlocktwo.flush(); 



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
	drv_qlocktwo.enable_element(y, x)

def wordOn(line, start, length):
	for i in range(start, start+length):
		on(i, line)

def allOff():
	for x in range(0, 12):
		for y in range(0, 11):
			off(x, y)

def off(x, y):
	demo.setColor(x, y, '#aaaaaa')


while True:
	tick()
	sleep(1)    