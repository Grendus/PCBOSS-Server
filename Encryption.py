import random
import keys
import Crypto.PublicKey.RSA
import Crypto.Hash.SHA512
from Crypto.Cipher import AES
from Crypto import Random

TOKEN_LENGTH = 16
KEY_LENGTH = 32
IV_LENGTH = 16

encryption_key = Crypto.PublicKey.RSA.importKey(keys.public_key)
decryption_key = Crypto.PublicKey.RSA.importKey(keys.private_key)

def pwdHash(pwd):
    #todo: add hash function
    hasher = Crypto.Hash.SHA512.new()
    hasher.update(pwd)
    return hasher.hexdigest()

def sessionToken():
    return ''.join([str(random.randint(0,10)) for x in range(TOKEN_LENGTH)])

"""
Messages can contain three different classes of value: dictionaries, lists, or values that 
can be cast to string. This recursively parses the message, encrypting each part of the message
while leaving the structure intact.
"""
def encryptEntrance(unencryptedFile):
	key = Random.new().read(KEY_LENGTH)
	encFile = encrypt(unencryptedFile, key)
	return {"key":encryption_key.encrypt(key,None)[0], "data":encFile}

def encryptFile(unencryptedFile, key):
	iv = Random.new().read(IV_LENGTH)
	aes_cipher = AES.new(key, AES.MODE_CFB, iv)
	message = iv+aes_cipher.encrypt(unencryptedFile)
	return message

def encryptDict(unencryptedDict, encryptionkey):
	encryptedDict = dict()
	for key, value in unencryptedDict.iteritems():
		encryptedDict[encrypt(key, encryptionkey)] = encrypt(value, encryptionkey)
	return encryptedDict

def encryptList(unencryptedList, key):
	encryptedList = list()
	for value in unencryptedList:
		encryptedList.append(encrypt(value, key))
	return encryptedList

def encrypt(unencryptedMessage, key):
	if type(unencryptedMessage) is dict:
		return encryptDict(unencryptedMessage, key)
	elif type(unencryptedMessage) is list:
		return encryptList(unencryptedMessage, key)
	else:
		return encryptFile(unencryptedMessage, key)

"""
Same as above, recursively decrypt the message sent. The logic is the same on both the
server and local system, just different keys.
"""
def decryptEntrance(encryptedFile):
	key = decryption_key.decrypt(encryptedFile["key"])
	return decrypt(encryptedFile["data"], key)

def decryptFile(encryptedFile, key):
	#generate an AES cipher using the initialization vector of the encrypted portion
	aes_cipher = AES.new(key, AES.MODE_CFB, encryptedFile[:16])
	return aes_cipher.decrypt(encryptedFile[16:])

def decryptDict(encryptedDict, encryptionKey):
	decryptedDict = dict()
	for key, value in encryptedDict.iteritems():
		decryptedDict[decrypt(key, encryptionKey)] = decrypt(value, encryptionKey)
	return decryptedDict

def decryptList(encryptedList, key):
	decryptedList = list()
	for value in encryptedList:
		decryptedList.append(decrypt(value, key))
	return decryptedList

def decrypt(encryptedMessage, key):
	if type(encryptedMessage) is dict:
		return decryptDict(encryptedMessage, key)
	elif type(encryptedMessage) is list:
		return decryptList(encryptedMessage, key)
	else:
		return decryptFile(encryptedMessage, key)
