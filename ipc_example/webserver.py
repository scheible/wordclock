import zmq
import time

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

message = input("Message: ")

# Immer Raw-Data senden, keine Strings
socket.send(message.encode('UTF-8'))
socket.RCVTIMEO = 1000

try:
	re = socket.recv()
	print("RETURN:", re)
except Exception as e:
	print(str(e))
	# Diese Exception wird geworfen bei einem Timeout