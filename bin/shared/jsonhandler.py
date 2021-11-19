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
				if (type(index) is int and index < len(obj[p])):
					obj[p].pop(index)
					somethingDone = True

	return somethingDone

def addSomethingToJson(obj, update):
	## only allow to add very specific fields to the json

	profileTemplate = {
        "userProfileEnabled": False,
        "startTime": {
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "stopTime": {
            "hours": 10,
            "minutes": 0,
            "seconds": 0
        },
        "config": {
            "isSoftTransitionEnabled": True,
            "transitionTimeMs": 500,
            "transitionMode": "exp",
            "colorBodyRGB": [
                255,
                255,
                255
            ],
            "brightnessBody": 50,
            "colorBorderRGB": [
                1,
                1,
                1
            ],
            "brightnessBorder": 255,
            "colorMinuteRGB": [
                100,
                0,
                0
            ],
            "brightnessMinute": 255,
            "colorSecondRGB": [
                20,
                20,
                20
            ],
            "brightnessSecond": 255,
            "isMinuteShown": True,
            "isSecondShown": True,
            "isBorderShown": True
        }
    }

	somethingDone = False
	if (update.get('userProfiles')):
		print("json handler: add new user profile")
		obj['userProfiles'].append(profileTemplate)
		somethingDone = True
	else:
		print("json handler: unknown add command")

	return somethingDone	