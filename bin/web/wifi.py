import subprocess

def listWifi():
	result = subprocess.check_output('sudo iw dev wlan0 scan ap-force | grep SSID', shell=True)
	sResult = result.decode('utf-8')
	wifiList = []
	for line in sResult.split('\n'):
		line = line.strip()
		if (len(line) > 7 and line[0] != '*'):
			wifiList.append(line[6:])

	return wifiList


def stopAP():
	result = subprocess.check_output('sudo ./stop_ap.sh', shell=True)

def startAP():
	result = subprocess.check_output('sudo ./start_ap.sh', shell=True)