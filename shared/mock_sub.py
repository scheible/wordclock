import ipc, json

communication = ipc.WebserverComponentIpcListener()


print("listening for new events...")
try:
	while True:
		state, data = communication.recv()
		if (state == ipc.NEW_JSON_AVAILABLE):
			print(json.dumps(json.loads(data), indent=3))
except KeyboardInterrupt:
	pass