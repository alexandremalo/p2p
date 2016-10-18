import socket

def download_file(filename, host, port):
	file = open("download/"+filename,'wb')
	file.write(get_socket_answer("GET_FILE "+filename, host, port))
	return None

def get_file_list(host, port):
	return get_socket_answer("GET_LIST", host, port)

def get_socket_answer(question, host, port):
	client_socket = socket.socket()
	client_socket.connect((host, port))
	client_socket.send(question)
	return client_socket.recv(1024)

#print get_socket_answer("GET_LIST", "localhost", 5001)
download_file("test123", "localhost", 5001)


