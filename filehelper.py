import hashlib
import ast
import os
import socket
import security as sec
from base64 import b64encode as base64encode
from base64 import b64decode as base64decode

def hashFile(filename):
	hasher = hashlib.md5()
	with open(filename,'rb') as afile:
		buf = afile.read()
		hasher.update(buf)
	return hasher.hexdigest()


def updateIndex(filename):
	with open("files.idx","a") as afile:
		afile.write(hashFile(filename)+" "+filename)
		afile.close()


def findFile(hashcode):
	afile = open("files.idx","r")
	lines = afile.readlines()
	afile.close()
	for line in lines:
		if line[:32] == hashcode:
			return line[33:]
	return False


def is_open(file_name):
    if os.path.exists(file_name):
        try:
            os.rename(file_name, file_name) #can't rename an open file so an error will be thrown
            return False
        except:
            return True
    raise NameError

def refreshIndex():
	afile = open("files.idx","w")
	for filename in os.listdir("Downloads"):
		afile.write(hashFile(filename)+" "+filename)

def receive_file(ip, port, my_private=None, node_pub=None, sock = None, node = None):
    l = 1
    cl = None
    if not sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,port))
        cl = 1
    sock.send("READY");
    l = sock.recv(1024)
    if node:
        l = str(node)
    f = open("Downloads/"+l,"wb")
    while l:
        l = sock.recv(1024)
        if my_private:
            tup = ast.literal_eval(str(l))
            l = sec.decrypt_message(tup,my_private,node_pub)
        if not l:
            f.close()
            sock.close()
            print("Message Altered !!!")
            break;
        if l == str.encode("ENDOFP2P"):
            break
        f.write(l)
    f.close()
    if cl :
        sock.close()

def send_file(name, port, my_private=None, node_pub=None, sock=None):
    cl = None
    conn = sock
    if not sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('',port))
        print("Waiting for connection ... ")
        cl = 1
    	sock.listen(1)
    	conn, adr = sock.accept()
    	print(adr)
    m = conn.recv(1024)
    if m == "READY":
        conn.send(name)
    try:
        f = open(name,"rb")
    except:
        print("File not found!!")
        return False
    l = f.read(1024)
    while l:
        if not my_private :
            enc = l
            conn.send(enc)
        else:
            enc = sec.encrypt_message(l,my_private,node_pub)
            conn.send(str(enc))
        l = f.read(1024)
    end=str.encode("ENDOFP2P")
    if my_private:
        end = sec.encrypt_message(end,my_private,node_pub)
        conn.send(str(end))
    else:
        conn.send(end)
    if cl :
    	conn.close()
        sock.close()
    return True

