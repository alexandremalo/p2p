import filehelper as fh
import security as sec
import os
import socket
import os.path

ROOT = os.path.dirname(os.path.realpath(__file__))

def send_file(filename, port, me):
	filename = ROOT + "/" + filename
	print filename
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('',port))
	sock.listen(1)
	conn, adr = sock.accept()
	m = conn.recv(1024)
	if m == "KILL":
		sock.close()
		return None
	fh.receive_file(None,None,sock=conn,node=m)
	conn.send(str(me))
	if not os.path.isfile(ROOT+"/keys/public.key"):
		sec.getPrivate()
	fh.send_file(ROOT+"/keys/public.key",None,sock=conn)
	fh.send_file(filename,None,sec.getPrivate(),sec.lookup_public_key(m),conn)
	conn.close()
	sock.close()
	os.remove(ROOT+"/Downloads/"+str(m))

def receive_file(ip,port,filename,me):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip,port))
	if os.path.isfile(ROOT+"/Downloads/"+filename) and fh.is_open(ROOT+"/Downloads/"+filename):
		sock.send("KILL")
		return None
	sock.send(str(me))
	if not os.path.isfile(ROOT+"/keys/public.key"):
		sec.getPrivate()
	fh.send_file(ROOT+"/keys/public.key",None,sock=sock)
	he = sock.recv(1024)
	fh.receive_file(None,None,sock=sock,node=he)
	fh.receive_file(None,None,sec.getPrivate(),sec.lookup_public_key(he),sock=sock)
	sock.close()
	os.remove(ROOT+"/Downloads/"+str(he))
	fh.refreshIndex()
