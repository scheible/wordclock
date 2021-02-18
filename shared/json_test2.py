def updateJsonArray(obj, update):
	somethingDone = False

	if not (type(obj) is list) or not (type(update) is list):
		return False

	for j, e in enumerate(update):
		if (type(e) is dict):
			if updateJson(obj[j], update[j]):
				somethingDone = True

		elif (type(e) is list):
			if updateJsonArray(obj[j], update[j]):
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


obj = {'name': 'patrik', 'data': 1, 'config': [{'id': 1,'farbe': [255, 255, 1], 'helligkeit': 14},{'id': 2, 'farbe': [255, 255, 1], 'helligkeit': 14}]}




print("Update top element")

update = {'data': 23}

print(obj)
print(updateJson(obj, update))
print(obj)

print("-----------------------")

print("Update 2 top elements at the same time")

update = {'data': 19, 'name': 'blub'}

print(obj)
updateJson(obj, update)
print(obj)

print("-----------------------")

# Erstes Array Element nicht ändern und nur den B wert der Farbe und die Helligkeit ändern

print("Update 2nd element of an array")
update = {'config': [{}, {'helligkeit': 9, 'farbe': [{},18]}]}

print(obj)
updateJson(obj, update)
print(obj)

print("-----------------------")

# das 'config' member ist im original ein array --> im update object ist config ein Object mit index member
# dieser Index wird gelöscht.
# --> Vorteil: es können auch integer aus einem Array gelöscht werden ohne ID

print("remove an array element")
update = {'config': {'index': 1}}

print(obj)
removeArrayElement(obj, update)
print(obj)