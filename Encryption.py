import random

def pwdHash(pwd):
    #todo: add hash function
    return pwd

def sessionToken():
    #todo: implement secure session ID generator
    sessionToken=""
    for x in range(16):
        sessionToken+=str(random.randint(0,9))
    return sessionToken

def encryptFile(unencryptedFile):
    #todo: add encryption
    return unencryptedFile
