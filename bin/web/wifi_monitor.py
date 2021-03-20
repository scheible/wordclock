#!../env/bin/python -u

import wifi, time

ap_state = False
old_ap_state = False
connection_state = ""
old_connection_state = ""

while True:
	ap_state = wifi.isAP()
	connection_state = wifi.getStatus()

	if (old_ap_state != ap_state):
		old_ap_state = ap_state

		if (ap_state == 'ap'):
			print("Access point started")

		elif (ap_state == 'no_ap'):
			print("Access point stopped")

		else:
			print("no idea?!??!!")

	if (old_connection_state != connection_state):
		old_connection_state = connection_state
		print(connection_state)


	time.sleep(0.1)