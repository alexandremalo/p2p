import socket
import glob
import os
import threading

from Node import Node
from RoutingTable import RoutingTable
from tcplisten import ThreadingExample

def init(my_id):
	rt = RoutingTable(my_id)
	return rt

def send_tcp_message(message, host, port, answer_needed=False):
        toReturn = None
        try:
                client_socket = socket.socket()
                client_socket.connect((host, port))
                client_socket.send(message)
        except:
                print "Error: Connection to server failed"
        if answer_needed:
                try:
                        toReturn = client_socket.recv(1024)
                except:
                        print "Error: Answer from server was expected :("
        return toReturn

def start(rt):
	answer = " "
	while answer != "3":
		print "1 - Normal mode"
        	print "2 - Debug mode"
		print "3 - Quit"
	        answer = raw_input("choose an option: ")
       		if answer == "1":
			var = raw_input("TCP PORT: ")
                        port = int(var)
                        listener = ThreadingExample(rt, port)
			answer_normal = " "
			while answer_normal != "3":
				print "1 - Join Cluster"
				print "2 - Create Cluster"
				print "3 - Back"
				answer_normal = raw_input("choose an option: ")
				if answer_normal == "1":
					ip = raw_input("IP: ")
					port = raw_input("Port: ")
					
				elif answer_normal == "2":
					print "New Cluster!!"
					while True:
						message = raw_input("Message: ")
						ip = raw_input("IP: ")
						port = raw_input("Port: ")
						print send_tcp_message(message, ip, int(port), False)
				message = raw_input("Send Message")
		elif answer == "2":
			print("debug_mode...")
	


print "starting P2P...."
rt = init("1")
start(rt)
