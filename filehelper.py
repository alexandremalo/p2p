import hashlib
import ast
import os
import socket
import security as sec
from base64 import b64encode as base64encode
from base64 import b64decode as base64decode

ROOT = os.path.dirname(os.path.realpath(__file__))

def hashFile(filename):
	hasher = hashlib.md5()
	filename = ROOT + "/" + filename
	with open(filename,'rb') as afile:
		buf = afile.read()
		hasher.update(buf)
	return hasher.hexdigest()


def updateIndex(filename):
	with open(ROOT+"/files.idx","a") as afile:
		afile.write(hashFile(filename)+" "+filename)
		afile.close()


def findFile(hashcode):
	afile = open(ROOT+"/files.idx","r")
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
	afile = open(ROOT+"/files.idx","w")
	for filename in os.listdir(ROOT+"/Shared"):
		afile.write(hashFile(filename)+" "+filename)

def receive_file(ip, port, my_private=None, node_pub=None, sock = None, node = None):
    l = 1
    cl = False
    if not sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,port))
        cl = True
    sock.send("READY")
    l = sock.recv(1024)
    if node:
        l = str(node)
    f = open(ROOT+"/Downloads/"+l,"wb")
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
        if l == "ENDOFP2P":
            break
        sock.send("\r\n\r\n")
        f.write(l)
    f.close()
    if cl :
        sock.close()

def send_file(name, port, my_private=None, node_pub=None, sock=None):
    cl = False
    conn = sock
    if not sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('',port))
        cl = True
    	sock.listen(1)
    	conn, adr = sock.accept()
    	print(adr)
    m = conn.recv(1024)
    print m
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
        conn.recv(1024)
        l = f.read(1024)
    end="ENDOFP2P"
    if my_private:
        end = sec.encrypt_message(end,my_private,node_pub)
        conn.send(str(end))
    else:
        conn.send(end)
    if cl :
    	conn.close()
        sock.close()
    return True

