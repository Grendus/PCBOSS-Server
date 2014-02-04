import Authentication

def getID(uname,pwd):
    return Authentication.authUser(uname,pwd)

def validateID(authToken):
    return Authentication.validateUser(authToken)

def requestJobHistory(authToken):
    return Authentication.authViewRequest(authToken)

def saveFile(ID, CADFile, filedesc):
    try:
        Authentication.authUpload(ID, CADFile, filedesc)
    except:
        return False
    return True

def getUsername(authToken):
    return Authentication.getUser(authToken)

def getUserInfo(authToken):
    return Authentication.getUserInfo(authToken)

def updateAccount(authToken, fname, lname, pwd1=False, pwd2=False):
    if pwd1 and pwd1 == pwd2:
        Authentication.updateAccount(authToken,fname, lname, pwd1)
    else:
        Authentication.updateAccount(authToken, fname, lname)

def endSession(authToken):
    Authentication.endSession(authToken)
