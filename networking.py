import socket
import glob
import os
import threading

from Node import Node
from RoutingTable import RoutingTable

def init(my_id):
	rt = RoutingTable(my_id)
	return rt

def join_cluster(ip):
	print send_message_to_directly_connected_node("JOIN::2::0::0")
	return None

def welcome_new_node():
	list_of_nodes = ""
	send_message_to_node(list_of_nodes)
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

def get_next_hop_to_node(node_id):
	return None

def add_next_hop_to_node():
	return None

def send_message_to_node(node_id, message):
	return None

def feed_paths_to_node(node_id, paths):
	return None

def evaluate_routing_table():
	return None

def sending_my_node_info(node_id, hops_to_node, connected_nodes_count, date_of_this_info):
	return None

def declare_dead_node(node_id):
	return None

def print_routing_table():
	print "not yet implemented"

def listen_for_questions(routing_table):
	rt = routing_table.get_table()
        receiver_socket = socket.socket()
        host = "0.0.0.0"
        port = 5001
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
			

def follow_message_to_connected_nodes(message, rt):
	new_message = message[0]+message[1]+str(int(message[2])+1)+message[3]
	message_all_connected_nodes(new_message, rt)

	
def message_all_connected_nodes(message, rt):
        list = get_directly_connected_host(rt)
        for entry in list:
                send_message_to_directly_connected_node(message, entry.get_ip(), 5001)

def get_directly_connected_host(rt):
	list_to_return = []
	for entry in rt:
		if entry.get_hops() == 1:
			list_to_return.append(entry)
	return list_to_return

def ask_question_to_node(question, id):
	return None

def send_message_to_node(message, id):
	return None

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
	print "1 - sender"
	print "else - receiver"
        var = raw_input("choose an option: ")
	if var == "1":
		test_message = raw_input("message: ")
		print send_message_to_directly_connected_node(test_message, "localhost", 5001, True)
	else:
		listen_for_questions(rt)
        return "Done"




print "starting P2P...."
rt = init("1")
print "Starting to listen"
#t = threading.Thread(target=listen_for_questions(rt), args=())
#t.daemon = True
#t.start()
#print "YES!"
test(rt)
