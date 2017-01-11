import sharefile as sf
import threading

while True:
	print "choose :"
	print "1 - Receive"
	print "2 - Send"
	n = int(input("Choice : "))
	i = int(input("id : "))
	if n == 1:
		sf.send_file("test.txt",9999)
	else :
		t = threading.Thread(target=sf.receive_file, args=("127.0.0.1",9999,"test.txt",i))
		t.start()
