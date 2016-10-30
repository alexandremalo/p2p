import socket
import glob
import os
import threading

from Node import Node
from p2pMec import RoutingTable
from tcplisten import ThreadingExample

def init(my_id):
	rt = RoutingTable(my_id)
	return rt

def join_cluster(ip, port):
	new_id, total_host = send_message_to_directly_connected_node("JOIN", ip, port, True)
	rt = new RoutingTable(new_id)
	get_nodes(ip, port, )	

def welcome_new_node():
	return None

def ping_directly_connected_nodes():
	message = "PING::0::0::0"
	list = get_directly_connected_host(rt)
	dead_nodes = []
        for entry in list:
                answer = send_message_to_directly_connected_node(message, entry.get_ip(), 5001, True)
		if answer.split("::")[0] == "PONG":
			print "stil up"
		else:
			dead_nodes.append(entry)
	for entry in dead_nodes:
		declare_dead_node(entry.get_node_id())
	return None

def listen_for_questions(routing_table, tcpport):
	rt = routing_table.get_table()
        receiver_socket = socket.socket()
        host = "0.0.0.0"
        port = tcpport
        receiver_socket.bind((host, port))
        receiver_socket.listen(5)
        while True:
                socket_obj, source = receiver_socket.accept()
                print "Connection from ", source
		source_IP = source[0]
                message = socket_obj.recv(1024)
		print message
		splitted_message = message.split("::")	
		if splitted_message[0] == "NEW":
			socket_obj.sendall("NEW::"+str(rt[0].get_node_id())+"::"+str(rt[0].get_hops())+"::"+str(rt[0].get_connected_nodes()))
			follow_message = routing_table.evaluate_new_request(splitted_message[1], splitted_message[2], splitted_message[3], source_IP)
			if follow_message:
				follow_message_to_connected_nodes(splitted_message, rt)
			routing_table.display_table()
			

def send_message_to_directly_connected_node(message, host, port, answer_needed=False):
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


def test(rt):
	var = raw_input("choose a TCP port: ")
	port = int(var)
	listen_for_questions(rt, port)
	listener = ThreadingExample(rt, port)
        return "Done"




