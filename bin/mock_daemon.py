import ipc, time, json


def updateJsonArray(obj, update):
	somethingDone = False

	for j, e in enumerate(update):
		if (type(e) is dict):
			if updateJson(obj[j], update[j]):
				somethingDone = True

		elif obj[j] != update[j]:
			obj[j] = update[j]
			somethingDone = True

	return somethingDone


def updateJson(obj, update):
	somethingDone = False

	if not (type(obj) is dict) or not(type(update) is dict):
		return False

	for p in update:
		if (p in obj):
			if type(obj[p]) is dict:
				if updateJson(obj[p], update[p]):
					somethingDone = True

			elif type(obj[p]) is list and type(update[p]) is list and len(obj[p]) >= len(update[p]):
				if updateJsonArray(obj[p], update[p]):
					somethingDone = True

			elif (obj[p] != update[p]):
				obj[p] = update[p]
				somethingDone = True

	return somethingDone

def removeArrayElement(obj, update):
	somethingDone = False

	for p in update:
		if (p in obj):
			if type(obj[p]) is dict:
				if removeArrayElement(obj[p], update[p]):
					somethingDone = True

			elif type(obj[p]) is list:
				index = update[p]['index']
				if (index < len(obj[p])):
					obj[p].pop(index)
					somethingDone = True

	return somethingDone


fileHandle = open("../Documentation/Cfg_Clock.json")
jConfig = json.load(fileHandle)
fileHandle.close()

communication = ipc.DaemonComponentIpcBindung()

print("Listening...")

try:
	while True:
		state, data = communication.receiveCommand(jConfig)

		if (state == ipc.NEW_JSON_AVAILABLE):
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