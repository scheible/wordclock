from flask import Flask, render_template, request, redirect
from random import randint
import time, json
from uhrthree import labersack, listwifi, timesettings

app = Flask(__name__)


@app.route('/timesettings', methods=['GET'])
def timeSettings():
	return render_template('timesettings.html')

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
	cat = request.form['category']
	zone = request.form['zone']
	timesettings.setTimezone(cat, zone)
	return render_template('timesettings_okay.html')


@app.route('/wifisetup/', methods=['GET'])
def index():
	print(request)
	return render_template('index.html')

@app.route('/listwifi', methods=['GET'])
def listWifi():
	availableAPs = listwifi.listWifi()
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

	listwifi.stopAP()

	return "<h1>Wifi Setup, please restart</h1>"


@app.route('/status/')
def status():
	return str(randint(0,100))

@app.route('/longpoll')
def blub():
	ev = labersack.EventClient()
	if (ev.tickUpdate()):
		return json.dumps({'state': 'ok', 'update': 1})
	else:
		return json.dumps({'state': 'ok', 'update': 0})

@app.route('/settings/')
def settings():
	return render_template('settings.html')

@app.route('/set/brightness', methods=['POST'])
def setBrigthness():
	data = request.json
	c = labersack.Client()

	if (c.setBrightness(data['brightness'])):
		return json.dumps({'state': 'ok'})
	return json.dumps({'state': 'failed'})

@app.route('/get/brightness', methods=['GET'])
def getBrigthness():
	c = labersack.Client()
	b = c.getBrightness()

	if (b != None):
		return json.dumps({'state': 'ok', 'brightness': b})
	else:
		return json.dumps({'state': 'failed'})

	
@app.route('/set/color/<field>', methods=["POST"])
def setRGBLetters(field):
	data = request.json
	func = None
	c = labersack.Client()

	func = getColorSetterFunction(field, c)
	if func == None:
		return json.dumps({'state': 'failed'})

	if (func(data['r'], data['g'], data['b'])):
		return json.dumps({'state': 'ok'})
	return json.dumps({'state': 'failed'})
	
@app.route('/get/color/<field>', methods=['GET'])
def getRGBLetters(field):
	c = labersack.Client()
	func = getColorGetterFunction(field, c)
	if (func == None):
		return json.dumps({'state': 'failed'})

	r, g, b = func()
	if (r != None):
		return json.dumps({'state': 'ok', 'r': r, 'g': g, 'b': b})
	else:
		return json.dumps({'state': 'failed'})


def getColorSetterFunction(field, client):
	if (field == 'letters'):
		return client.setLetterColor
	elif (field == 'frame'):
		return client.setFrameColor
	elif (field == 'minutes'):
		return client.setMinutesColor
	elif (field == 'seconds'):
		return client.setSecondsColor
	else:
		return None

def getColorGetterFunction(field, client):
	if (field == 'letters'):
		return client.getLetterColor
	elif (field == 'frame'):
		return client.getFrameColor
	elif (field == 'minutes'):
		return client.getMinutesColor
	elif (field == 'seconds'):
		return client.getSecondsColor
	else:
		return None

# This will catch all paths that are not valid
# So at any random url we will end up at the wifi
# setup. This is what Captive Portal clients will do
# It sucks if the user has a typo or so though
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def test(path):
	return redirect('/wifisetup')



if __name__ == "__main__":
	app.run(debug=True, host="127.0.0.1", port=8080)