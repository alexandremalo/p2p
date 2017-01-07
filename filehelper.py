import hashlib
import os

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


def refreshIndex():
	afile = open("files.idx","w")
	for filename in os.listdir("Downloads"):
		afile.write(hashFile(filename)+" "+filename)

def receive_file(ip, port):
    l = 1
    socket = socket.socket()
    socket.connect((ip,port))
    l = socket.recv(1024)
    f = open(l,"wb")
    while l:
        f.write(l)
        l = socket.recv(1024)
        if l == str.encode("ENDOFP2P"):
            break
    f.close()

def send_file(name, port):
    try:
        conn = socket.socket()
        conn.bind(('',port))
		m = conn.recv(1024)
		if m == "READY":
			conn.send(name)
        f = open(name,"rb")
        l = f.read(1024)
        while l:
            conn.send(l)
            l = f.read(1024)
        conn.send(str.encode("ENDOFP2P"))
        return True
    except:
        print("File not found!!")
        return False

