import threading
import time
import network

from network import *

class diagnostic(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, rt, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
	self.routing_table = rt
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
		time.sleep(1)
		take_action_thread = threading.Thread(target=self.take_action, args=())
                take_action_thread.start()

    def take_action(self):
                ping_directly_connected_nodes(self.routing_table)






#example = ThreadingExample()
#time.sleep(3)
#print('Checkpoint')
#time.sleep(5)
#print('Bye')
