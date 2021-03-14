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