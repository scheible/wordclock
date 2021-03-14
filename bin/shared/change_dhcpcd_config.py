import sys

fileName = '/etc/dhcpcd.conf'
fileHandle = open(fileName, 'r')
fileContent = fileHandle.read()
fileHandle.close()
fileHandle = open(fileName, 'w')

if (len(sys.argv) < 2):
	print("Usage:", sys.argv[0], "<static/dhcp>")
	exit(1)

for line in fileContent.split('\n')[:-1]:
	if (line == 'interface wlan0' or line == '#interface wlan0' or\
		line == 'static ip_address=192.168.17.1/24' or line == '#static ip_address=192.168.17.1/24' or \
		line == 'nohook wpa_supplicant' or line == '#nohook wpa_supplicant'):

			if (line[0] == '#'):
				line = line[1:]

			print(line)

			if (sys.argv[1] == 'static'):
				fileHandle.write(line + '\n')
			else:
				fileHandle.write('#' + line + '\n')
	else:
		fileHandle.write(line + '\n')

fileHandle.close()