import shared.ipc, json
import time

communication = shared.ipc.WebserverComponentIpcSender()

#jsonString = '{asdfasdf}'
#jsonString = open("cfg/update.json").read()
jsonString = open("cfg/update3.json").read()
#jsonString = '{"commandType": "query"}'
#jsonString = '{"commandType": "remove", "dat": {"userProfiles": {"index": 0}}}'

r = communication.send(jsonString)
#r = communication.send(jsonString2)
print(r)

#print(json.dumps(json.loads(r), indent=3))
