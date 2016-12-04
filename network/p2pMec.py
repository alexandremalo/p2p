from Node import Node

class RoutingTable:
	tableCount = 0
	def __init__(self, my_id, my_port, total_host):
		self.my_id = my_id
		self.table = []
		self.total_host = total_host
		self.my_port = my_port
		#this_node = Node(my_id, my_id, "127.0.0.1", my_port)
		#self.table.append(this_node)

	def get_table(self):
		return self.table

	def get_node_info(self, id):
		IptoReturn = None
		#self.display_table()
		PorttoReturn = None
		found = False
		for node in self.table:
			#print node.get_node_id()
			if int(node.get_node_id()) == int(id):
				found = True
				IptoReturn = node.get_node_ip()
				PorttoReturn = node.get_node_port()
		#print IptoReturn
		#print PorttoReturn
		return IptoReturn, PorttoReturn

	def adding_new_node(self):
		self.total_host += 1

	def display_table(self):
		print "table:"
		print "My_id: "+str(self.my_id)
		for entry in self.table:
			print entry.get_node_id(), entry.get_node_ip(), entry.get_node_port()
		return None


	def find_closest_node_to(self, id):
		if id > self.total_host:
                        print "Invalid ID..."
                        return None

                mat_closest = self.my_id
		real_closest = self.my_id
		best_available_closest = self.my_id
                distance = id - self.my_id
                if distance < 0:
                        distance = self.total_host + distance
                        print "passing by 0"
                #print distance
                i = 0
                while 2**i <= distance:
                        mat_closest = (2**i + self.my_id) % self.total_host
			#print "Mat_Closest: "+str(mat_closest)
			exists = False
			best_choice = distance
			for entry in self.table:
				if int(entry.get_node_id()) == int(mat_closest):
					exists = True
				#else:
					#temp_distance = entry.get_node_id() - self.my_id
					#if temp_distance < 0:
					#	temp_distance = self.total_host + temp_distance
					#if temp_distance > max and temp_distance < 2**i:
					#	real_closest = entry.get_node_id()
			if exists == True:
				best_available_closest = mat_closest
			#else:
			#	best_available_closest = real_closest
                        i += 1
		#print "BAC: "+str(best_available_closest)
		return best_available_closest

	def get_needed_nodes(self):
		i = 0
		list_of_needed_nodes = []
		while 2**i < self.total_host:
			list_of_needed_nodes.append((2**i+self.my_id) % self.total_host)
			i += 1
		return list_of_needed_nodes

			
	def add_new_node(self, id, id_closest, ip, port):
		new_node = Node(id, id_closest, ip, port)
		self.table.append(new_node)
		return None

	def get_my_id(self):
		return self.my_id

	def set_my_id(self, id):
		self.my_id = id

	def get_my_port(self):
		return self.my_port

	def get_total_host(self):
		return self.total_host
	
	def set_total_host(self, x):
		self.total_host = x
