import socket

def test(test):
        receiver_socket = socket.socket()
        host = "localhost"
        port = 5001
        receiver_socket.bind((host, port))
        receiver_socket.listen(5)
        while True:
                socket_obj, source = receiver_socket.accept()
                print "Connection from ", source
		incomplete_payload = socket_obj.recv(1024)
		socket_obj.sendall("HelloWorld2U2!")
		complete_payload = ""
		incomplete = True
		while incomplete:
			print "Receiving..."
			complete_payload += incomplete_payload
			print incomplete_payload
                        print "Total = ", complete_payload
			incomplete_payload = socket_obj.recv(1024)
			if not incomplete_payload:
				incomplete = False
		print "Done!"
		if complete_payload == "HelloWorld!":
			print "Trying to send back infos"
			socket_obj.sendall("HelloWorld2U2!")
			print "Did it!"
		elif complete_payload == "gimmeafile":
			socket_obj.sendall("HereIsABigFile")
		#socket_obj.send("OK!")



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

