import socket
import sys
import os
import tqdm

# create server socket
s = socket.socket()
print("Socket is successfully created")

# socket bind port 9800
s.bind(('', 9800))

# receive 4096 bytes each time
BUFFER_SIZE = 4096

SEPARATOR = "<SEPARATOR>"

# server is able to accept connection
s.listen(5)
print(f"Server is listening...")

# accept connections if there is any
client, address = s.accept()

# if client is connected
print("Client is connected!")

# receive the file infos
# receive using client  socket (not server socket)
received = client.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

# remove absolute path if there is
filename = os.path.basename(filename)

# convert file to integer
filesize = int(filesize)

# start receiving the file from the client
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = 1024)
with open(filename, "wb") as f:
	for _ in progress:
		# read 1024 bytes from the socket (receive)
		bytes_read = client.recv(BUFFER_SIZE)
		if not bytes_read:
			break

		# write the file received
		f.write(bytes_read)

		# update the progress bar
		progress.update(len(bytes_read))

# close client and server
client.close()
s.close()
