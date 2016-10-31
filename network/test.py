from  p2pMec import RoutingTable

def find_closest_node_to(id, my_id, total_host):
                if id >= total_host:
                        print "Invalid ID..."
                        return None

                closest = my_id
                distance = id - my_id
                if distance < 0:
                        distance = total_host + distance
			print "passing by 0"
		print distance
                i = 0
                while 2**i <= distance:
                        print 2**i
                        closest = (2**i + my_id) % total_host
                        i += 1
                return closest

rt = RoutingTable(1, 1, 4)
rt.add_new_node(2, 2, "node2", 2)
rt.add_new_node(0, 0, "node0", 0)

rt.display_table()
rt.find_closest_node_to(3)

test = 3-4 % 5
print test
#print find_closest_node_to(2,5,11)


