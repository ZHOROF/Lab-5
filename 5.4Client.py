import socket
import sys
import os
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# create client socket
s = socket.socket()

# the ip address of server
host = '10.0.2.16'

# the port
port = 9800

# connect to socket
print(f"Connecting to ({host}: Port: {port})") 
s.connect((host, port))
print("Connected.")

# prompt filename from user
filename = input("Enter the filename with extension: ")
print("Filename : ", filename)

# get the file size
filesize = os.path.getsize(filename)

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

#start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit = "B", unit_scale = True, unit_divisor = 1024)
with open(filename, "rb") as f:
	for _ in progress:
		# read the bytes from the file
		bytes_read = f.read(BUFFER_SIZE)
		if not bytes_read:
			# file transmitting is done
			break
		# we use sendall to assure transmission in
		# busy networks
		s.sendall(bytes_read)

		# update the progress bar
		progress.update(len(bytes_read))
# close socket
s.close()
