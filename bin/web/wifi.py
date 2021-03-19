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

def connectToAP(ssid, pw):
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

	stopAP()
