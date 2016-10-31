import socket
import glob
import os
import threading

from Node import Node
from p2pMec import RoutingTable

def new_cluster(my_port):
	rt = RoutingTable(0, my_port, 1)
	return rt

def join_cluster(ip, port, my_port):
	completeanswer = send_message_to_directly_connected_node("JOIN::"+str(my_port), ip, port, True)
	while completeanswer.split("|_|")[0].split("::")[0] == "REDIRECT":
		completeanswer = send_message_to_directly_connected_node("JOIN::"+str(my_port), completeanswer.split("::")[1], int(completeanswer.split("::")[2]), True)
	answer = completeanswer.split("|_|")[0]
        new_id = answer.split("::")[1]
        rt = None

	if answer.split("::")[0] == "WELCOME":
		rt = RoutingTable(int(answer.split("::")[1]), my_port, int(answer.split("::")[1])+1)
	if int(rt.get_total_host()) == 2 and int(rt.get_my_id()) == 1:
		rt.add_new_node(0, 0, ip, port)
	rt.display_table()
	return rt

def welcome_new_node(rt, ip, port):
	rt.set_total_host(rt.get_total_host()+1)
	new_id = str(rt.get_total_host()-1)
	basic_reply = "WELCOME::"+str(new_id)
	routing_table_dump = "|_|TABLE|_|"
	for node in rt.get_table():
		entry = ""
		if node.get_node_id() != rt.get_my_id():
			entry = str(node.get_node_id())+"__"+str(node.get_closest_to())+"__"+str(node.get_node_ip())+"__"+str(node.get_node_port())
		routing_table_dump += entry
	rt.add_new_node(new_id, new_id, ip, port)
	rt.display_table()
	return basic_reply+routing_table_dump

def take_action_on_message(string, rt, ip):
	split_message = string.split("::")
	if split_message[0] == "JOIN":
		if rt.get_my_id() == rt.get_total_host() - 1:
			#rt.set_total_host(rt.get_total_host()+1)
			#return "WELCOME::"+str(rt.get_total_host()-1)
			return welcome_new_node(rt, ip, split_message[1])
		else:
			ip, port = rt.get_node_info(rt.find_closest_node_to(rt.get_total_host() - 1))
			return "REDIRECT::"+str(ip)+"::"+str(port)


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


def send_message_to_directly_connected_node(message, host, port, answer_needed=False):
        toReturn = None
	try:
		client_socket = socket.socket()
       		client_socket.connect((host, int(port)))
       		client_socket.send(message)
	except:
		print "Error: Connection to server failed on "+host+str(port)
	if answer_needed:
		try:
			toReturn = client_socket.recv(1024)
		except:
			print "Error: Answer from server was expected :("
        return toReturn




