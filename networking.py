import socket
import glob
import os

def join_cluster(ip):
	return None

def connect_directly_to_nodes():
	return None

def welcome_new_node():
	list_of_nodes = ""
	send_message_to_node(list_of_nodes)

def get_list_of_directly_connected_nodes():
	return None

def ping_directly_connected_nodes():
	return None

def get_next_hop_to_node(node_id):
	return None

def add_next_hop_to_node():
	return None

def send_message_to_node(node_id, message):
	return None

def feed_paths_to_node(node_id, paths)
	return None

def evaluate_routing_table():
	return None

def sending_my_node_info(node_id, hops_to_node, connected_nodes_count, date_of_this_info):
	return None

def declare_dead_node(node_id):
	return None

def print_routing_table():
	print "not yet implemented"

def listen_for_questions():
        receiver_socket = socket.socket()
        host = "172.20.20.20"
        port = 5001
        receiver_socket.bind((host, port))
        receiver_socket.listen(5)
        while True:
                socket_obj, source = receiver_socket.accept()
                print "Connection from ", source
                message = socket_obj.recv(1024)
		print message
		socket_obj.sendall("Hello")

def ask_question_to_node(question, id):
	return None

def send_message_to_node(message, id):

def ask_question_to_directly_connected_node(question, host, port):
        client_socket = socket.socket()
        client_socket.connect((host, port))
        client_socket.send(question)
        return client_socket.recv(1024)

def send_message_to_directly_connected_node(message, host, port):
	client_socket = socket.socket()
        client_socket.connect((host, port))
        client_socket.send(message)

print "starting P2P...."



