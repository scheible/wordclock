import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
	try:
		#NOBLOCK flag!!!
		message = socket.recv(flags=zmq.NOBLOCK)
		print("RCV:",message)

		if (message == b"exit"):
			break

		time.sleep(1)
		socket.send(b"okay")
	except Exception as e:
		# Diese Excp wird geworfen, wenn keine Daten vorhanden
		# sind (also fast immer). Hier einfach warten.
		time.sleep(0.1)


socket.close()