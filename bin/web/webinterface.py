import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from flask import Flask, render_template, request, redirect
import time, json, logging
import timesettings, wifi
import shared.ipc as ipc


app = Flask(__name__)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/mainview')
def index():
	return render_template('index.html')

@app.route('/testing/startap')
def testing_startap():
	app.logger.info('starting wifi access point')
	wifi.startAP()
	return "ok"

@app.route('/testing/stopap')
def testing_stopap():
	wifi.stopAP()
	return "ok"

@app.route("/set", methods=["POST"])
def set():
	communication = ipc.WebserverComponentIpcSender()
	data = request.json
	r = communication.send(json.dumps(data))
	return r


@app.route("/state")
def getState():
	communication = ipc.WebserverComponentIpcSender()
	jsonString = '{"commandType": "query"}'

	r = communication.send(jsonString)
	if (r == 'error'):
		answer = {'state': 'failed', 'update': 0, 'errorText': 'daemon does not answer'}
	else:
		try:
			answer = {'state': 'ok', 'update': 1, 'data': json.loads(r)}
		except:
			answer = {'state': 'failed', 'update': 0, 'errorText': 'daemon returned malformed json'}
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
	availableAPs = None
	counter = 0
	while availableAPs == None:
		availableAPs = wifi.listWifi()
		counter+=1

		if counter > 5:
			return json.dumps(['<error loading wifi list>'])

	return json.dumps(availableAPs)

@app.route('/wifisetup', methods=['POST'])
def wifiSetup_post():

	answer = {'state': 'ok', 'update': 0}
	try:
		data = request.json
		ssid = data['ssid']
		pw = data['pw']

		print("setting wifi with")
		print("ssid    ", ssid)
		print("password", pw)

		wifi.connectToAP(ssid, pw)
	except:
		answer = {'state': 'failed', 'update': 0, 'errorText': 'provided wrong json'}

	return answer


# This will catch all paths that are not valid
# So at any random url we will end up at the wifi
# setup. This is what Captive Portal clients will do
# It sucks if the user has a typo or so though
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def test(path):
	return redirect('/mainview')



if __name__ == "__main__":
	app.run(debug=True, host="localhost", port=8080)