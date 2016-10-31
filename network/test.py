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


#print find_closest_node_to(2,5,11)


test = "test113"
print test.split(",")[0]
