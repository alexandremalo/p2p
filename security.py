from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 
from Crypto import Random
from base64 import b64decode
from base64 import b64encode
import os.path
from Crypto.Hash import SHA256

def encrypt_message(message, my_privatekey, node_publickey):
	sha = SHA256.new(message)
	signer = PKCS1_v1_5.new(my_privatekey)
	encrypted = node_publickey.encrypt(message,32)
	encHash = signer.sign(sha)
	return (encrypted,b64encode(encHash))

def decrypt_message(enc_msg, my_privatekey, node_publickey):
	msg = my_privatekey.decrypt(enc_msg[0])
	verifier = PKCS1_v1_5.new(node_publickey)
	sha = SHA256.new(msg)
	if not verifier.verify(sha,b64decode(enc_msg[1])):
		return None
	return msg

def encrypt_message_for_node(node_id, message):
	pub_key = lookup_public_key(node_id)
	my_priv = getPrivate()
	return encrypt_message(message,my_priv,pub_key)

def decrypt_message_from_node(node_id, message):
	pub_key = lookup_public_key(node_id)
	my_priv = getPrivate()
	return decrypt_message(message, my_priv, pub_key)

def getPrivate():
	if os.path.isfile('keys/private.key') :
		RSA_key = readfile('keys/private.key')
		RSA_key = RSA.importKey(RSA_key)
		return RSA_key
	else:
		random_generator = Random.new().read
		key = RSA.generate(1024, random_generator)
		pke = key.exportKey(format='PEM')
		writefile('keys/private.key', pke)
		pke = key.publickey().exportKey(format='PEM')
		writefile('keys/public.key',pke)
		return getPrivate()

def readfile(name):
	f = open(name,'rb')
	return f.read()

def writefile(name,obj):
	f = open(name, 'wb')
	f.write(obj)
	f.close()

#TODO : change this function to support lookup for node's public key using routing table
def lookup_public_key(node_id):
	if os.path.isfile('keys/public.key'):
		RSA_key = readfile('keys/public.key')
		RSA_key = RSA.importKey(RSA_key)
		return RSA_key
	else:
		getPrivate()
		return lookup_public_key(node_id)


def receivefile(self, ip, port, data):
    f = open(data,"wb")
    l = 1
    l = socket.recv(1024)
    while l:
        print(l)
        f.write(l)
        l = self.socket.recv(1024)
        if l == str.encode("ENDOFKEY"):
            break
    f.close()

def sendfile(self,conn,name):
    try:
        f = open(name,"rb")
        l = f.read(1024)
        while l:
            conn.send(l)
            l = f.read(1024)
        return True
    except:
        print("File not found!!")
        return False

msg = "hello"
enc_msg = encrypt_message_for_node(1,msg)
print(enc_msg)
dec_msg = decrypt_message_from_node(1,enc_msg)
print(dec_msg)

