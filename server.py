import socket
import glob
import os


def give_list(dir):
	#return glob.glob(dir)
	#os.listdir("/home/alex/Documents/enseirb/p2p/*")
	return next(os.walk(dir))[2]

def give_file(filename):
	dir = "/home/alex/Documents/enseirb/p2p/"
	file = open(""+dir+filename,'rb')
	payload = file.read(1024)
	file.close()
	return payload

def test(test):
        receiver_socket = socket.socket()
        host = "localhost"
        port = 5001
        receiver_socket.bind((host, port))
        receiver_socket.listen(5)
        while True:
                socket_obj, source = receiver_socket.accept()
                print "Connection from ", source
		message = socket_obj.recv(1024)
		if message == "HelloWorld!":
			socket_obj.sendall("HelloWorld2U2!")
		elif message == "GET_LIST":
			print give_list("/home/alex/Documents/enseirb/p2p")
			for item in give_list("/home/alex/Documents/enseirb/p2p"):
				socket_obj.sendall(item + "  ")
		elif message.split(" ", 1)[0] == "GET_FILE":
			socket_obj.sendall(give_file(message.split(" ", 1)[1]))
		else:
			socket_obj.sendall("Invalid command on the server")


print "Welcome to you my friend, please choose an option:"
print "1 - Try connecting to a distant host"
print "2 - Open incoming secure socket"
action = 0;

while action == 0:
        var = raw_input("Please enter something: ")
        if var == "1":
                print "remote connection"
                action = 1
                break
        elif var == "2":
                print "Openning secure socket"
                action = 2
                test("test")
        else:
                print "Invalid Input"
