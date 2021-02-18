import json

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
				for j, e in enumerate(update[p]):
					if (type(e) is dict):
						updateJson(obj[p][j], e)
					else:
						print("[DEBUG][update array value] ", "obj[", p, "][", j, "]=", obj[p][j], " --> ", e, sep="")
						obj[p][j] = e

			elif (obj[p] != update[p]):
				print("[DEBUG][update object value] ", "obj[", p, "]=", obj[p], " --> ", update[p], sep="")
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



obj = {'State': 'ok', 'names': [1, 3], 'app': {'id': 1, 'name': 2}, 'list': [{'name': 'nix'}, {'name': 'nix'}, {'name': 'nix'}]}
update = {'list': [{}, {'name': 'blub'}]}

print(obj)

#updateJson(obj, update)
updateJson(obj, update)


print(obj)

update = {'list': [{}, {'name': 'pat'}]}
updateJson(obj, update)


print(obj)