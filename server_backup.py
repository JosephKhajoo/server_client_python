import threading
import socket
import sys

HEADER = 64
PORT = 5050

# Getting the ip address of the server by getting the hostname of the computer,
# and then getting the ip address of that hostname
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

CLOSE_MESSAGE = "!SHUTDOWN"
ALL_MESSAGES = []
# Making an endpoint
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the endpoint to the server and port,
# so that anything that passes through the ip address also hits the socket
server.bind(ADDR)

# Function that handles the clients that connected to our server 
def handle_client(conn, addr):

	name = conn.recv(1048)

	if name:
		name = name.decode(FORMAT)
	print(f"[NEW CONNECTION] {addr} - {name} connected.")

	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			ALL_MESSAGES.append(msg)
			print(f"[{name}]: {msg}")
			if msg == DISCONNECT_MESSAGE:
				print(f"[DISCONNECTED] '{name}'")
				connected = False

			if msg == CLOSE_MESSAGE:
				server.close()
				sys.exit(0)
	print(ALL_MESSAGES)
	conn.close()


# Function that starts listening for connections
def start():
	print("[STARTING] Starting the server...")
	
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
	while True:

		# Getting the information about the connection,
		# and the socket object (conn) so that we can send information back
		conn, addr = server.accept() 
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()

		# Printing the number of active connections at the moment
		print(f"[ACTIVE] {threading.activeCount() - 1}")


try:
	start()
except Exception as e:
	print("[ERROR] Could not start the server because of the following error:" + "\n" + str(e))