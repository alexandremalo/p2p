from Node import Node

class RoutingTable:
	tableCount = 0
	def __init__(self, my_id):
		self.table = []
		this_node = Node(my_id, 0, 0)
		self.table.append(this_node)

	def get_table(self):
		return self.table
	
	def display_table(self):
		print "table:"
		for entry in self.table:
			print entry.get_node_id(), entry.get_hops(), entry.get_connected_nodes()
		return None

	def hello_received(self, id, hops, connected):
		return None
		
	def evaluate_new_request(self, node_id, hops, connected_nodes):
		already_exist = False
		for entry in self.table:
			if(node_id == entry.get_node_id()):
				already_exist = True
				if(hops < entry.get_hops() or connected_nodes != entry.get_connected_nodes()):
					entry = Node(node_id, hops, connected_nodes)
		if already_exist == False:
			self.table.append(Node(node_id, hops, connected_nodes))
