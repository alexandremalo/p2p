import socket
import glob
import os
import threading
import network
import time

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import filehelper as fh
from Node import Node
from p2pMec import RoutingTable
from tcplisten import ThreadingExample
from diag import diagnostic
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


def menu_down(me):
	while True:
		print("What do you want ")
		print("1 - Download file ")
		print("2 - Ping node ")
		c = int(raw_input("Choice : "))
		if c == 2:
			node = raw_input("Node id :")
			if node != "":
				answer = send_ping_to_id(int(node), rt)
			print(answer)
		elif c == 1:
			hash = raw_input("Hash :")
			down_file(me,hash)

def start():
	answer = " "
	while answer != "3":
		fh.refreshIndex()
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
					pinger = diagnostic(rt)
					print " "
					print "Welcome in Cluster !!"
					menu_down(rt)
				elif answer_normal == "2":
                    			rt = new_cluster(listenerPort)
					listener = ThreadingExample(rt, listenerPort)
					pinger = diagnostic(rt)
					print " "
                    			print "New Cluster!!"
					while True:
                        			node = raw_input(" ")
                        			#message = raw_input("Message: ")
                        			#answer = send_message_to_id(int(node), rt, message)
                        			if node != "":
							answer = send_ping_to_id(int(node), rt)
                        				print answer
		elif answer == "2":
			print("debug_mode...")
			while True:
                                  message = raw_input("Message: ")
                                  ip = raw_input("IP: ")
                                  port = raw_input("Port: ")
                                  send_tcp_message(message, ip, int(port), False)



print "starting P2P...."
start()
