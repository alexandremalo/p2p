class Node:
	nodeCount = 0
	
	def __init__(self, node_id, hops, connected):
		self.node_id = node_id
		self.ip = None
		self.hops = hops
		self.connected = connected
		Node.nodeCount += 1

	def get_node_id(self):
		return self.node_id

	def get_hops(self):
		return self.hops
	
	def get_connected_nodes(self):
		return self.connected
		
	def get_node_ip(self):
		return self.ip
