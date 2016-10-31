import socket
import glob
import os
import threading
import network

from Node import Node
from p2pMec import RoutingTable
from tcplisten import ThreadingExample
from network import *

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

def start():
	answer = " "
	while answer != "3":
		print "1 - Normal mode"
        	print "2 - Debug mode"
		print "3 - Quit"
	        answer = raw_input("choose an option: ")
       		if answer == "1":
			var = raw_input("TCP PORT: ")
                        listenerPort = int(var)
			answer_normal = " "
			while answer_normal != "3":
				print "1 - Join Cluster"
				print "2 - Create Cluster"
				print "3 - Back"
				answer_normal = raw_input("choose an option: ")
				if answer_normal == "1":
					ip = raw_input("IP: ")
					port = raw_input("Port: ")
					rt = join_cluster(ip, port, listenerPort)
					listener = ThreadingExample(rt, listenerPort)
					print(" ")
				elif answer_normal == "2":
					print "New Cluster!!"
					rt = new_cluster(listenerPort)
					listener = ThreadingExample(rt, listenerPort)
					print(" ")
					while True:
						message = raw_input("Message: ")
						ip = raw_input("IP: ")
						port = raw_input("Port: ")
						print send_tcp_message(message, ip, int(port), False)
		elif answer == "2":
			print("debug_mode...")
			while True:
                                  message = raw_input("Message: ")
                                  ip = raw_input("IP: ")
                                  port = raw_input("Port: ")
                                  print send_tcp_message(message, ip, int(port), False)
	


print "starting P2P...."
start()
