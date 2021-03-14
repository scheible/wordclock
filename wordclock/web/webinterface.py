import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from flask import Flask, render_template, request, redirect
from random import randint
import time, json
import wifi, timesettings
import shared.ipc as ipc


app = Flask(__name__)


@app.route('/mainview')
def index():
	return render_template('index.html')


@app.route("/set", methods=["POST"])
def set():
	communication = ipc.WebserverComponentIpcSender()
	data = request.json
	print(data)
	r = communication.send(json.dumps(data))
	print(r)
	return r


@app.route("/state")
def getState():
	communication = ipc.WebserverComponentIpcSender()
	jsonString = '{"commandType": "query"}'

	r = communication.send(jsonString)
	if (r == None):
		answer = {'state': 'failed', 'update': 0, 'errorText': 'daemon does not answer'}
	else:
		answer = {'state': 'ok', 'update': 1, 'data': json.loads(r)}
	return json.dumps(answer)


@app.route('/longpoll')
def blub():
	communication = ipc.WebserverComponentIpcListener()

	state, data = communication.recv()
	if (state == ipc.NEW_JSON_UPDATE):
		r = json.loads(data)
		answer = {'state': 'ok', 'update': 1, 'data': r}
		return json.dumps(answer)
	else:
		return json.dumps({'state': 'ok', 'update': 0})


@app.route('/timesettings/timezonecategories', methods=['GET'])
def getTimezoneCategories():
	cats = timesettings.getTimezoneCategories()
	cats.sort()
	return json.dumps(cats)

@app.route('/timesettings/timezones/<zone>', methods=['GET'])
def getTimezones(zone):
	zones = timesettings.getTimezones(zone)
	zones.sort()
	return json.dumps(zones)

@app.route('/timesettings/timezone', methods=['POST'])
def setTimezone():
	data = request.json
	cat = data['category']
	zone = data['timezone']

	print(cat)
	print(zone)

	timesettings.setTimezone(cat, zone)
	return json.dumps({'state': 'ok'})


@app.route('/listwifi', methods=['GET'])
def listWifi():
	#availableAPs = listwifi.listWifi()
	time.sleep(2)
	availableAPs = ['test1', 'test2', 'test3']
	return json.dumps(availableAPs)

@app.route('/wifisetup/', methods=['POST'])
def wifiSetup_post():
	print("DEBUGGING")
	ssid = request.form['ssid']
	pw = request.form['password']
	print("setting wifi with")
	print("ssid    ", ssid)
	print("password", pw)

	fileHandle = open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
	fileHandle.write('country=DE\n')
	fileHandle.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
	fileHandle.write('update_config=1\n')
	fileHandle.write('network={\n')
	fileHandle.write('ssid="' + ssid + '"\n')
	fileHandle.write('scan_ssid=1\n')
	fileHandle.write('psk="' + pw + '"\n')
	fileHandle.write('key_mgmt=WPA-PSK\n')
	fileHandle.write('}\n')
	fileHandle.close()

	wifi.stopAP()

	return "<h1>Wifi Setup, please restart</h1>"


# This will catch all paths that are not valid
# So at any random url we will end up at the wifi
# setup. This is what Captive Portal clients will do
# It sucks if the user has a typo or so though
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def test(path):
	return redirect('/mainview')



if __name__ == "__main__":
	app.run(debug=True, host="192.168.0.199", port=8080)