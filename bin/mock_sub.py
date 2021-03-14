import shared.ipc, json

communication = shared.ipc.WebserverComponentIpcListener()


print("listening for new events...")
try:
	while True:
		state, data = communication.recv()
		if (state == shared.ipc.NEW_JSON_UPDATE):
			print(json.dumps(json.loads(data), indent=3))
except KeyboardInterrupt:
	pass