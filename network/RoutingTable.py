from Node import Node

class RoutingTable:
	tableCount = 0
	def __init__(self, my_id):
		self.my_id = my_id
		self.table = []
		this_node = Node(my_id, my_id, my_id+1, "localhost")
		self.table.append(this_node)

	def get_table(self):
		return self.table
	
	def display_table(self):
		print "table:"
		for entry in self.table:
			print entry.get_node_id(), entry.get_hops(), entry.get_connected_nodes(), entry.get_next_hop()
		return None

	def hello_received(self, id, hops, connected):
		return None
		
	def evaluate_new_request(self, node_id, hops, connected_nodes, source_ip):
		already_exist = False
		newTable = self.table
		table_modified = False
		for entry in self.table:
			if(node_id == entry.get_node_id()):
				already_exist = True
				if(int(hops) +1 < entry.get_hops() or int(connected_nodes) != entry.get_connected_nodes()):# or source_ip == entry.get_next_hop()):
					newTable.remove(entry)
					newTable.append(Node(node_id, int(hops)+1, int(connected_nodes), source_node))
					table_modified = True
		if already_exist == False:
			self.table.append(Node(node_id, int(hops)+1, int(connected_nodes), source_ip))
			table_modified = True
		self.table = newTable
		return table_modified

