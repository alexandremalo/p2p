import sharefile as sf
import threading
import filehelper as fh

fh.refreshIndex()


'''
while True:
	print "choose :"
	print "1 - Send"
	print "2 - Receive"
	n = int(input("Choice : "))
	i = int(input("id : "))
	if n == 1:
		p = int(input("Port : "))
		sf.send_file("test.txt",p,i)
	else :
		p = int(input("Port : "))
		t = threading.Thread(target=sf.receive_file, args=("127.0.0.1",p,"test.txt",i))
		t.start()
		t.join()

'''
