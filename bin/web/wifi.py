import subprocess


def getStatus():
	# COMPLETED: connceted to a wiif
	# DISCONNECTED: could mean connection went wrong or in AP mode
	# SCANNING
	# ASSOCIATING
	# UNKNOWN: some error occured and we don't know the state


	try:
		result = subprocess.check_output('wpa_cli -i wlan0 status | grep wpa_state', shell=True)
		sResult = result.decode('utf-8').strip()
		state = sResult.split('=')
		if (len(state) == 2):
			return state[1]
		else:
			return "UNKNOWN"

	except:
		return "UNKNOWN"

def isAP():
	try:
		result = subprocess.check_output('systemctl status hostapd | grep Active:', shell=True)
		sResult = result.decode('utf-8').strip()
		isActive = sResult.split(' ')
		if (len(isActive) >= 2):
			isActive = isActive[1]
			if (isActive == "active"):
				return "ap"
			else:
				return "no_ap"
		return "unknown"
	except:
		return "unknown"

def listWifi():
	try:
		result = subprocess.check_output('sudo iw dev wlan0 scan ap-force | grep SSID', shell=True)
		sResult = result.decode('utf-8')
		wifiList = []
		for line in sResult.split('\n'):
			line = line.strip()
			if (len(line) > 7 and line[0] != '*'):
				wifiList.append(line[6:])
	except:
		wifiList = None

	return wifiList

def stopAP():
	try:
		result = subprocess.check_output('sudo ./stop_ap.sh', shell=True)
	except:
		pass

def startAP():
	try:
		result = subprocess.check_output('sudo ./start_ap.sh', shell=True)
	except:
		pass

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
