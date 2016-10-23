import threading
import time
import socket

class SocketListening(object):
	def __init__(self):
		self.thread = None
        	#thread = threading.Thread(target=self.run, args=())
        	#thread.daemon = True                            # Daemonize thread
        	#thread.start()                                  # Start the execution

	def run(self):
        	""" Method that runs forever """
		receiver_socket = socket.socket()
        	host = "0.0.0.0"
        	port = 5001
        	receiver_socket.bind((host, port))
        	receiver_socket.listen(1)
        	while True:
                	socket_obj, source = receiver_socket.accept()
               		print "Connection from ", source
                	source_IP = source[0]
                	message = socket_obj.recv(1024)
                	print message

	def listen():
		self.thread = threading.Thread(target=self.run, args=())
                thread.daemon = True                            # Daemonize thread
                thread.start()


example = SocketListening()
print('YES!')
time.sleep(3)
print('Checkpoint')
time.sleep(50)
print('Bye')
