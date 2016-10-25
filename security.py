#Every host ID will be associate with a public/private key.
#So everytime you want to talk to a host in the cluster, you need to know their public KEY
#Ex:  If you join the cluster by connecting to 3 computers, you need to download the 3 public keys
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from Crypto import Random
from base64 import b64decode
import os.path
import hashlib

def encrypt_message(message, my_privatekey, node_publickey):
	sha = hashlib.new('sha256')
	sha.update(message)
	msgHash = sha.hexdigest()
	encrypted = node_publickey.encrypt(message,32)
	encHash = my_privatekey(message,0)
	return (encrypted,encHash)

def decrypt_message(enc_msg, my_privatekey, node_publickey):
	sha = hashlib.new('sha256')
	msg = my_privatekey.decrypt(enc_msg[0])
	msgReceivedHash = node_publickey.decrypt(enc_msg[1])
	sha.update(msg)
	msghash = sha.hexdigest()
	if msghash != msgReceivedHash:
		return None
	return msg

def encrypt_message_for_node(node_id, message):
	pub_key = lookup_public_key(node_id)
	my_priv = getPrivate()
	return encrypt_message(message,my_priv,pub_key)

def decrypt_message_for_node(node_id, message):
	pub_key = lookup_public_key(node_id)
	my_priv = getPrivate()
	return decrypt_message(message, my_priv, pub_key)

def getPrivate():
	if os.path.isfile("private.key") :
		RSAkey = readfile('private.key')
		RSAkey = RSA.importKey(RSAkey)
		return RSAkey
	else:
		random_generator = Random.new().read
		key = RSA.generate(1024, random_generator)
		pke = key.exportKey(format='PEM')
		writefile('private.key', pke)
		return getPrivate()
