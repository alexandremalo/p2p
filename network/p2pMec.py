from Node import Node

class RoutingTable:
	tableCount = 0
	def __init__(self, my_id, my_port, total_host):
		self.my_id = my_id
		self.table = []
		self.total_host = total_host
		self.my_port = my_port
		this_node = Node(my_id, my_id, "127.0.0.1", my_port)
		self.table.append(this_node)

	def get_table(self):
		return self.table

	def get_node_info(id):
		IptoReturn = None
		PorttoReturn = None
		for node in self.table:
			if entry.get_node_id() == id:
				IptoReturn = entry.get_node_ip()
				PorttoReturn = entry.get_node_port()
				break
		return IptoReturn, PorttoReturn

	def adding_new_node(self):
		self.total_host += 1

	def display_table(self):
		print "table:"
		for entry in self.table:
			print entry.get_node_id(), entry.get_closest_to(), entry.get_node_ip(), entry.get_node_port()
		return None


	def find_closest_node_to(id):
		if id >= self.total_host:
                        print "Invalid ID..."
                        return None

                closest = self.my_id
                distance = id - self.my_id
                if distance < 0:
                        distance = self.total_host + distance
                        print "passing by 0"
                print distance
                i = 0
                while 2**i <= distance:
                        print 2**i
                        closest = (2**i + self.my_id) % self.total_host
                        i += 1
                if i == distance:
			print "Direct connected"
		return closest
		
		
	

