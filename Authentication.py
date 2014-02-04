import Encryption
import Database

"""
Since we only expect to have a few users at any given time, we can cache the valid tokens
and save on datastore access.

This does mean that every time the server crashes everyone will have to log back in. Again,
given that we expect to have few users online at any given point this shouldn't be an issue.
"""


#todo: tokens should expire at some point. Valid workaround involves restarting the server daily
validTokens = {}

def authUser(uname, pwd):
    pwdHash = Encryption.pwdHash(pwd)
    if Database.isValid(uname,pwdHash):
        token = Encryption.sessionToken()

        #It's almost impossibly unlikely that we'll wind up with two identical tokens,
        #but if we did, it would be a hard bug to find.
        while token in validTokens:
            token = Encryption.sessionToken()
        validTokens[token] = uname
        return token
    return False

def validateUser(token):
    return token in validTokens

def authViewRequest(token):
    if token in validTokens:
        return Database.getJobs(getUser(token))

def authUpload(ID, CADFile, filedesc):
    #todo: figure out how to authenticate the file
    encFile = Encryption.encryptFile(CADFile)
    Database.storeFile(getUser(ID), encFile, filedesc)

def getUser(token):
    return validTokens[token]

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
        del validTokens[token]
