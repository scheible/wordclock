import shared.ipc, json

communication = shared.ipc.WebserverComponentIpcSender()

#jsonString = '{asdfasdf}'
jsonString = open("cfg/update.json").read()
jsonString2 = '{"commandType": "query"}'
#jsonString = '{"commandType": "remove", "data": {"userProfiles": {"index": 0}}}'

r = communication.send(jsonString)
#r = communication.send(jsonString2)
print(json.dumps(json.loads(r), indent=3))