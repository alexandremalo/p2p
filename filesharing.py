import socket
import glob
import os

def give_list(dir):
	return next(os.walk(dir))[2]

def give_file(filename):
	dir = "shared/"
	file = open(""+dir+filename,'rb')
	payload = file.read(1024)
	file.close()
	return payload

def test(test):
        receiver_socket = socket.socket()
        host = "172.20.20.20"
        port = 5001
        receiver_socket.bind((host, port))
        receiver_socket.listen(5)
        while True:
                socket_obj, source = receiver_socket.accept()
                print "Connection from ", source
		message = socket_obj.recv(1024)
		if message == "GET_LIST":
			print give_list("shared")
			for item in give_list("shared"):
				socket_obj.sendall(item + "  ")
		elif message.split(" ", 1)[0] == "GET_FILE":
			socket_obj.sendall(give_file(message.split(" ", 1)[1]))
		else:
			socket_obj.sendall("Invalid command on the server")


def download_file(filename, host, port):
        file = open("download/"+filename,'wb')
        file.write(get_socket_answer("GET_FILE "+filename, host, port))
	print filename+ " was succefully downloaded!!"
        return None

def get_file_list(host, port):
        return get_socket_answer("GET_LIST", host, port)

def get_socket_answer(question, host, port):
        client_socket = socket.socket()
        client_socket.connect((host, port))
        client_socket.send(question)
        return client_socket.recv(1024)

#print get_socket_answer("GET_LIST", "localhost", 5001)
#download_file("test123", "localhost", 5001)

#get_socket_answer("GET_LIST", 172.20.17.18, 5001)

print "Welcome to you my friend, please choose an option:"
print "1 - Try connecting to a distant host"
print "2 - Open incoming secure socket"


action = 0;
while action == 0:
        var = raw_input("Please enter something: ")
        if var == "1":
                print "remote connection"
                action = 1
		distant_info = 0
		client_menu = 0
		distant_host = ""
		distant_port = 0
		while client_menu == 0:
			if distant_info == 0:
				print "Please enter the peer information"
				distant_host = raw_input("Please enter the remote host IP: ")
				distant_port = raw_input("Please enter the remote host Port: ")
				print "We did not test if this is a valid host yet ..."
				distant_info = 1
			print "Please choose an option:"
			print "1 - List the availables files"
			print "2 - Download a given file"
			print "3 - Exit the client menu"
			client_choice = raw_input("choose an option: ")
			if client_choice == "1":
				try:
					distant_port = int(distant_port)
				        print get_socket_answer("GET_LIST", distant_host, distant_port)
				except:
					print "We are sorry... the host is unavailable"
			elif client_choice == "2":
				file_name = raw_input("Please enter the name of the file: ")
				try:
					download_file(file_name, distant_host, distant_port)
				except:
					print "We are sorry... the host is unavailable"
			elif client_choice == "3":
				client_menu = 1
			else:
				print "Invalid choice"
                break
        elif var == "2":
                print "Openning secure socket"
                action = 2
                test("test")
        else:
                print "Invalid Input"
