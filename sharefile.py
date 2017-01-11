import filehelper as fh
import security as sec
import os


def send_file(filename, port, node):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('',port))
	sock.listen(1)
	conn, adr = sock.accept()
	m = conn.recv(1024)
	if m == "KILL":
		sock.close()
		return None
	fh.receive_file(None,None,sock=conn,node=node)
	fh.send_file(filename,None,sec.getPrivate(),sec.lookup_public_key(node),conn)
	conn.close()
	sock.close()
	os.remove("Downloads/"+node+".key")

def receive_file(ip,port,filename,me):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip,port))
	if fh.is_open(filename)
		sock.send("KILL")
		return None
	sock.send(me)
	fh.send_file("keys/public.key",None,sock=sock)
	fh.receive_file(None,None,sec.getPrivate(),sec.lookup_public_key(),sock=sock)
	sock.close()
	fh.refreshIndex()
