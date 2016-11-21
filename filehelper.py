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
	return false


def refreshIndex():
	afile = open("files.idx","w")
	for filename in os.listdir(directory):
		afile.write(hashFile(filename)+" "+filename)


