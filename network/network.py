import socket
import glob
import os
import threading
import time

from Node import Node
from p2pMec import RoutingTable

def new_cluster(my_port):
	rt = RoutingTable(0, my_port, 1)
	return rt

def join_cluster(ip, port, my_port):
	completeanswer, ip, port = send_message_unkown_node("JOIN::"+str(my_port), ip, port, True)
	answer = completeanswer.split("|_|")[0]
        new_id = answer.split("::")[1]
        rt = None
	if answer.split("::")[0] == "WELCOME":
		rt = RoutingTable(int(answer.split("::")[1]), my_port, int(answer.split("::")[1])+1)
	i = 0
	while 2**i <= int(rt.get_total_host()):
		if 2**i == int(rt.get_my_id()):
			rt.add_new_node(int(rt.get_my_id())-1, int(rt.get_my_id())-1, ip, port)
		i += 1
	routing_table_dump = completeanswer.split("|_|")
	i = 2
	while i < len(routing_table_dump):
		entry_temp = routing_table_dump[i].split("__")
		rt.add_new_node(int(entry_temp[0]), int(entry_temp[1]), entry_temp[2], int(entry_temp[3]))
		i += 1
	rt.display_table()
	announce_myself(rt)
	return rt

#def update_rt_for_new_node(node_ip, rt, ip, port):
#		return None


def send_message_unkown_node(message, ip, port, need_answer=False):
	#print "Sent question: "+message
	completeanswer = send_message_to_directly_connected_node(message, ip, port, need_answer)
	if completeanswer != None:
		#print "Answer Received: "+completeanswer
		while completeanswer.split("|_|")[0].split("::")[0] == "REDIRECT":
                	ip = completeanswer.split("::")[1]
                	port = int(completeanswer.split("::")[2])
                	completeanswer = send_message_to_directly_connected_node(message, ip, port, need_answer)
			if completeanswer == None:
				completeanswer = "None::None"
		if completeanswer != "None::None":
			return completeanswer, ip, port
		else:
			return None, ip, port
	else:
		print "Error invalid answer from directly connected node ...."
		return None, None, None


def add_node_id_to_rt(node_id, rt):
	ip, port = rt.get_node_info(rt.find_closest_node_to(node_id))
	if ip != None and port != None:
		answer, ip, port = send_message_unkown_node("FIND::"+str(node_id), ip, int(port), True)
		if answer != None:
			if answer.split("::")[0] == "FOUND":
				rt.add_new_node(node_id, node_id, ip, port)
			#print "OK!!! adding new entry to rt: "
			#rt.display_table()

def ping_direct_node(node_id, node_ip, node_port, rt):
	change = False
	up = False
	answer, ip, port = send_message_unkown_node("PING::"+str(node_id), node_ip, int(node_port), True)
	if ip != None and port != None:
		if ip != node_ip or int(node_port) != int(port):
			up = True
	if answer != None:
		if answer.split("::")[0] == "PONG":
			if ip != node_ip or int(port) != int(node_port):
				change = True
				for entry in rt.get_table():
					if int(entry.get_node_id()) == int(node_id) and entry.get_node_ip() == node_ip and int(entry.get_node_port()) == int(node_port):
						entry.set_node_ip(ip)
						entry.set_node_port(int(port))
						print "Learning node change during Diag... new RT:"
						rt.display_table()
		up = True 
	return up

def send_ping_to_id(node_id, rt):
	send_message_to_id(node_id, rt, "PING::"+str(node_id))

def send_message_to_id(node_id, rt, message):
	ip, port = rt.get_node_info(rt.find_closest_node_to(node_id))
	try:
		answer, ip, port = send_message_unkown_node(message, ip, int(port), True)
		#print "Message received: "+answer+"  |  ip: "+ip+"  port: "+str(port)
	except:
		print "Invalid answer"


def repopulate_rt(rt, desire_size):
	print "list of nodes wanted: "+str(rt.get_needed_nodes())
	for id in rt.get_needed_nodes():
		found = False
		for entry in rt.get_table():
			if int(entry.get_node_id()) == int(id):
				#print "already exist:"
				found = True
		if found == False:
			add_node_id_to_rt(id, rt)
			#print "success to add id: "+str(id)
	#print "new table after addons: "
	#rt.display_table()
	for entry in rt.get_table():
		entry_needed = False
		for id in rt.get_needed_nodes():
			if int(entry.get_node_id()) == int(id):
				entry_needed = True
		if entry_needed == False:
			rt.get_table().remove(entry)
	print "NEW RT: "
	rt.display_table()


def announce_myself(rt):
	message = "JOINED::"+str(rt.get_my_id())+"::"+str(rt.get_my_port())
	message_all_nodes(message, rt)


def message_all_nodes(message, rt):
	for entry in rt.get_table():
		if int(entry.get_node_id()) != int(rt.get_my_id()):
			send_message_to_directly_connected_node(message, entry.get_node_ip(), int(entry.get_node_port()))

def welcome_new_node(rt, ip, port):
	rt.set_total_host(rt.get_total_host()+1)
	new_id = str(rt.get_total_host()-1)
	basic_reply = "WELCOME::"+str(new_id)
	routing_table_dump = "|_|TABLE"
	for node in rt.get_table():
		entry = ""
		if node.get_node_id() != rt.get_my_id():
			entry = "|_|"+str(node.get_node_id())+"__"+str(node.get_closest_to())+"__"+str(node.get_node_ip())+"__"+str(node.get_node_port())
		routing_table_dump += entry
	rt.add_new_node(new_id, new_id, ip, port)
	repopulate_rt(rt, rt.get_total_host())
	rt.display_table()
	return basic_reply+routing_table_dump

def take_action_on_message(string, rt, ip):
	split_message = string.split("::")
	if split_message[0] == "JOIN":
		if rt.get_my_id() == rt.get_total_host() - 1:
			return welcome_new_node(rt, ip, split_message[1])
		else:
			ip, port = rt.get_node_info(rt.find_closest_node_to(rt.get_total_host() - 1))
			return "REDIRECT::"+str(ip)+"::"+str(port)
	elif split_message[0] == "JOINED":
		if int(split_message[1]) +1 > int(rt.get_total_host()):
			#print "Need to update my table"
			rt.adding_new_node()
			repopulate_rt(rt, int(split_message[1])+1)
			message_all_nodes(string, rt)
		#else:
			#print "Already know about that..."
	elif split_message[0] == "FIND":
		if rt.get_my_id() == int(split_message[1]):
			return "FOUND"
		else:
			ip, port = rt.get_node_info(rt.find_closest_node_to(int(split_message[1])))
			return "REDIRECT::"+str(ip)+"::"+str(port)
	elif split_message[0] == "PING":
                if rt.get_my_id() == int(split_message[1]):
                        return "PONG"
                else:
                        ip, port = rt.get_node_info(rt.find_closest_node_to(int(split_message[1])))
                        return "REDIRECT::"+str(ip)+"::"+str(port)
	elif split_message[0] == "SEARCH":
		node = int(split_message[1])
		hash = split_message[2]
	elif split_message[0] == "GIVEME":
		node = int(split_message[1])
		hash = split_message[2]
		file_search = findFile(hash)
		if file_search == False:
			message_all_nodes(string)
			return "DISPACHED"
		port = random_port()
		send_file(file_search,port)
		return "COMEGETIT::"+str(my_ip())+str(port)
		#TODO : my ip and random port AND use function from parent directory : these two functions are in filehelper
	elif split_message[0] == "COMEGETIT":
		ip = int(split_message[1])
		port = split_message[2]
		receive_file(ip,port)
	elif split_message[0] == "DEAD":
		node = int(split_message[1])
		ip = split_message[2]
		port = int(split_message[3])
		size = int(split_message[4])
		evaluate_dead_node(rt, node, ip, port, size)
	return "No_answer_needed"

def evaluate_dead_node(rt, node, ip, port, size):
	declare_dead_node(rt, node, ip, port, size)

def ping_directly_connected_nodes(rt):
	#print "MY ID IS: ", rt.get_my_id()
        for entry in rt.get_table():
                if int(entry.get_node_id()) != int(rt.get_my_id()):
			message = "PING::"+str(entry.get_node_id())
                        print "PING..."
			#answer = send_message_to_directly_connected_node(message, entry.get_node_ip(), int(entry.get_node_port()), True)
			answer2 = ping_direct_node(int(entry.get_node_id()), entry.get_node_ip(), int(entry.get_node_port()), rt)
			if answer2:
				print "Not Dead yet..."
			else:
				count = 0
				while count > 0 and answer == None:
					time.sleep(0.2)
					answer = send_message_to_directly_connected_node(message, entry.get_node_ip(), int(entry.get_node_port()), True)
					count -= 1
				if count == 0:
					declare_dead_node(rt, entry.get_node_id(), entry.get_node_ip(), entry.get_node_port(), int(rt.get_total_host())-1)
	#fighting racing conditions:
	repopulate_rt(rt, rt.get_total_host())
	return None

def declare_dead_node(rt, node, ip, port, size):
	found = False
	#print "Looking for deletion...."
	rt.display_table()
	for entry in rt.get_table():
                if int(entry.get_node_id()) == int(node) and ip == entry.get_node_ip() and int(port) == int(entry.get_node_port()):
                        found = True
			rt.get_table().remove(entry)
			print "Found for deletion ..."
			rt.display_table()
	if found or int(size) < int(rt.get_total_host()):
		for entry in rt.get_table():
			if int(entry.get_node_id()) > int(node):
				entry.set_node_id(int(entry.get_node_id())-1)
				print "decrement node in table ...."
		if found:
			message_all_nodes("DEAD::"+str(node)+"::"+ip+"::"+str(port)+"::"+str(int(rt.get_total_host())-1), rt)
		if int(node) < int(rt.get_my_id()):
			rt.set_my_id(int(rt.get_my_id())-1)
		rt.set_total_host(int(rt.get_total_host())-1)
		repopulate_rt(rt, rt.get_total_host())


def send_message_to_directly_connected_node(message, host, port, answer_needed=False):
        toReturn = None
	try:
		client_socket = socket.socket()
       		client_socket.connect((host, int(port)))
       		client_socket.send(message)
	except:
		print "Error: Connection to server failed on "+str(host)+str(port)
	if answer_needed:
		try:
			toReturn = client_socket.recv(1024)
		except:
			print "Error: Answer from server was expected :("
        return toReturn
