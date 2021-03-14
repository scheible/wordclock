import ipc, json

communication = ipc.WebserverComponentIpcSender()

#jsonString = '{asdfasdf}'
#jsonString = open("command.json").read()
jsonString = '{"commandType": "query"}'
#jsonString = '{"commandType": "remove", "data": {"userProfiles": {"index": 0}}}'

r = communication.send(jsonString)
print(json.dumps(json.loads(r), indent=3))