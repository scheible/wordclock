import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import shared.ipc as ipc
import time, json
from shared.jsonhandler import *


fileHandle = open("Cfg_Clock.json")
jConfig = json.load(fileHandle)
fileHandle.close()

communication = ipc.DaemonComponentIpcBindung()

print("Listening...")

try:
	while True:
		state, data = communication.receiveCommand(jConfig)

		if (state == ipc.NEW_JSON_UPDATE):
			print("[set]", data)
			if updateJson(jConfig, data):
				communication.sendCommand(jConfig)

		elif (state == ipc.NEW_JSON_REMOVE):
			print("[remove]", data)
			if removeArrayElement(jConfig, data):
				communication.sendCommand(jConfig)

		elif (state == ipc.NEW_JSON_ADD):
			print("[add]", data)

		elif (state ==ipc.DATA_QUERY):
			print("[data query]")

		else:
			time.sleep(0.5)

except KeyboardInterrupt:
	pass