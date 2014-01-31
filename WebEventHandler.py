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
