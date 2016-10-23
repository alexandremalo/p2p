class Node:
	nodeCount = 0
	
	def __init__(self, node_id, hops, connected, next_hop):
		self.node_id = node_id
		self.ip = None
		self.hops = hops
		self.connected = connected
		self.next_hop= next_hop
		Node.nodeCount += 1

	def get_node_id(self):
		return self.node_id

	def get_hops(self):
		return self.hops
	
	def get_connected_nodes(self):
		return self.connected
	
	def set_node_ip(self, ip_addr):
		self.ip = ip_addr
	
	def get_node_ip(self):
		return self.ip

	def get_next_hop(self):
		return self.next_hop
