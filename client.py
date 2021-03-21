from termcolor import colored

import socket
import sys

HEADER = 64
PORT = 5050

SERVER = '192.168.0.249'

ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CLOSE_MESSAGE = "!SHUTDOWN"

NAME = input("Enter your name: ")
while not NAME:
	NAME = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	client.connect(ADDR)
	print(f"[CONNECTED] {SERVER}:{PORT} Connected")
except ConnectionRefusedError:
	print("[ERROR] Server is not running...")
	sys.exit(0)

client.send(NAME.encode(FORMAT))

def send_message(msg):
	
	# Encoding the (string) type message into (bytes)
	# so we can send it through the socket 
	message = msg.encode(FORMAT)
	
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)

	# Padding the length message so its always 64 bytes
	send_length += (b' ' * (HEADER - len(send_length)))
	
	# Sending the length of the message first
	client.send(send_length)
	client.send(message)


while True:
	try:
		to_send = input("Me:> ")
		send_message(to_send)
		if to_send == DISCONNECT_MESSAGE or to_send == CLOSE_MESSAGE:
			break

		# server_resp = client.recv(500)
		# print(server_resp.decode(FORMAT))

	except KeyboardInterrupt:
		send_message(DISCONNECT_MESSAGE)
		sys.exit(0)