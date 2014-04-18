import Encryption
import Database
from google.appengine.api import memcache
"""
Since we only expect to have a few users at any given time, we can cache the valid tokens
and save on datastore access.

This does mean that every time the server crashes everyone will have to log back in. Again,
given that we expect to have few users online at any given point this shouldn't be an issue.
"""

KEY_STORE_TIME = 3600

def authUser(uname, pwd):
    pwdHash = Encryption.pwdHash(pwd)
    if Database.isValid(uname,pwdHash):
        token = Encryption.sessionToken()

        #It's almost impossibly unlikely that we'll wind up with two identical tokens,
        #but if we did, it would be a hard bug to find.
        while not memcache.get(token) == None:
            token = Encryption.sessionToken()
        memcache.set(key=token, value=uname, time=KEY_STORE_TIME)
        return token
    return False

def validateUser(token):
    return not memcache.get(token) == None

def authViewRequest(token):
    if memcache.get(token):
        return Database.getJobs(getUser(token))

def authUpload(ID, CADFile, filedesc):
    #todo: figure out how to authenticate the file
    encFile = CADFile
    Database.storeFile(getUser(ID), encFile, filedesc)

def getUser(token):
    return memcache.get(token)

def getUserInfo(token):
    return Database.getUserInfo(getUser(token))

def updateAccount(token, fname, lname, pwd=False):
    if pwd:
        pwdHash = Encryption.pwdHash(pwd)
        Database.updateAccount(getUser(token), fname, lname, pwdHash)
    else:
        Database.updateAccount(getUser(token), fname, lname)

def endSession(token):
    if token in validTokens:
        memcache.delete(token)
