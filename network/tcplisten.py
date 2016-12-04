import threading
import time
import socket
import network

from Node import Node
from network import *

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, rt, tcpport=5500, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
	self.routing_table = rt
        self.interval = interval
	self.port = tcpport
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
	receiver_socket = socket.socket()
        host = "0.0.0.0"
        port = self.port
        receiver_socket.bind((host, port))
        receiver_socket.listen(100)
        while True:
        	#print('Listen for incomming tcp messages on :'+host+":"+str(self.port))
                socket_obj, source = receiver_socket.accept()
                #print "Connection from ", source
                source_IP = source[0]
                message = socket_obj.recv(1024)
                #print "I received: "+message
		#reply = take_action_on_message(message, self.routing_table, source_IP)
		#if reply != "No_answer_needed":
			#print "I will reply :"+reply
			#socket_obj.sendall(reply)
		take_action_thread = threading.Thread(target=self.take_action, args=(message, self.routing_table, source_IP, socket_obj))
                take_action_thread.start()

    def take_action(self, message, rt, source_IP, socket_obj):
                reply = take_action_on_message(message, self.routing_table, source_IP)
                if reply != "No_answer_needed":
                        #print "I will reply :"+reply
                        socket_obj.sendall(reply)






#example = ThreadingExample()
#time.sleep(3)
#print('Checkpoint')
#time.sleep(5)
#print('Bye')
