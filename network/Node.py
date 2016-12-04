class Node:
	nodeCount = 0
	
	def __init__(self, node_id, closest_to, ip, port):
		self.node_id = node_id
		self.ip = ip
		self.port = port
		self.closest_to = closest_to
		Node.nodeCount += 1

	def get_node_id(self):
		return self.node_id

	def get_node_ip(self):
		return self.ip

	def set_node_id(self, id):
		self.node_id = int(id)

	def get_node_port(self):
		return self.port
		
	def get_closest_to(self):
		return self.closest_to
